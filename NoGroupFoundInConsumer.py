#!/usr/bin/python3
import subprocess
import sys
#import Convertor
#import Mailer
import os
import re,time

#change Directory to script location
scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)

#Declaraions
dc_name=os.uname()[1].split('-')[1]
lagScriptLoc="/home/azureuser/workdir/ccscgfeastus2prodstfs001-prod-01/kafka_scripts/"
scripName="getKafkaConsumerGroupLag_CC_all.sh"
consumerGroups={"odf-streamer-pst-daily-streamer":"cgf-ngm-streamer-pst-daily-prod","odf-streamer-pst-subscription":"cgf-ngm-streamer-pst-subscription-prod","odf-streamer-spr":"cgf-ngm-streamer-spr-prod"}
sendMail=False

#Email File
html_file='mail_alert.html'
FROM="DL-ATTCCSOPS@att.com"
TO="shivalsh@amdocs.com"
#TO="SmartOpsATTCCSOPS@amdocs.com ATTCCSOPS@amdocs.com"

writer=open(html_file, 'w')
writer.write('''<!DOCTYPE html>
        <html>
        <head>
        <style>
        td {
          text-align: center;
          }
          </style>
          </head>''')
writer.write("<h3>Comsumer Lag Check | {}</h3>\n".format(dc_name.upper()))
writer.write("<body><table border=\"1\">\n")
writer.write("<tr><th colspan=\"6\">Streamer Lag Status</th></tr>\n")
writer.write("<tr><th>Sno.</th><th>Consumer Name</th><th>LAG</th><th>Old Streamer PodName</th><th>New Streamer PodName</th><th>New Pod Status</th></tr>\n")



#html_content = "<html><head><title></title></head><body>\n"

def checkConsumerLag():
    sno=1
    ns="cgf"
    #HeaderDataList=[]
    #issue_data_list = []
    global html_content
    global sendMail
    #convert = Convertor
    #con = convert.Convert()
    #html_content = html_content + "<table border=\"1\"; width=\"70%\">\n"
    #HeaderDataList=["Sno.","Consumer Name","LAG","Old Streamer PodName","New Streamer PodName","New Pod Status"]
    #header_record = con.list2html(HeaderDataList, True)
    #html_content += header_record
    for key in consumerGroups.keys():
        print("Streamer is= ",key)
        print("Consumer is= ",consumerGroups[key])
        res=subprocess.getoutput('cd {0} ;./{1} {2} '.format(lagScriptLoc,scripName,consumerGroups[key]))
        print("\n----------------------\n",res)

        # if "has no active members"
        match = re.search(r'has no active members', res)
        if match:
            print("String 'has no active members' found")
            # Check the lag string
            lag = re.search(r'Total message LAG :: (\d+)', res)
            if lag:
                # get the value of lag
                lag_value = lag.group(1)
                print(f"Lag value: {lag_value}")
                # Check if value of lag is > 0 the restart the streamer
                if int(lag_value) > 0:
                    sendMail = True
                    #Get the pod name to restart
                    pod=subprocess.getoutput("/usr/local/bin/kubectl get pods -n {0}| grep -i '{1}' | awk '{{print $1}}'".format(ns,key))
                    print("The Streamer Pod Name is= ",pod)
                    # Get pod Logs 
                    st,logs=subprocess.getstatusoutput("/usr/local/bin/kubectl logs {0} -n {1} > {2}.log".format(pod,ns,key))
                    if st == 0:
                        print("Logs Taken successfully")
                    # call function to restart the streamer
                    val=restarStreamer(pod,key)
                    writer.write("<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(sno,consumerGroups[key],lag_value,pod,val[0],val[1]))
                    writer.write("</table></body></html>\n")
                    #issue_data =[sno,consumerGroups[key],lag_value,pod,val[0],val[1]]
                    #issue_data_list.append(issue_data)
                    sno+=1
                    print("\n=============================================================\n")
            else:
                print("Lag value not found")
        else:
            print("String 'has no active members' not found")
    
    #print("Issue data list is= ",issue_data_list)
    writer.close()
    '''
    if sendMail:
        for issue_record in issue_data_list:
                html_content = html_content + con.list2html(issue_record)
        html_content = html_content + '</table></body></html>'
    print("Mail Contenet is = ",html_content)
    '''
    print("function ends")
                
def restarStreamer(pod,key):
    ns="cgf"
    print("Pod to restart is = ",pod)
    # Delete the existing pod
    command1 = "/usr/local/bin/kubectl delete pod {0} -n {1}".format(pod,ns)
    print("Command to delete pod is= ",command1)
    #subprocess.run(command1, shell=True)

    # Sleep for 2 minutes
    print("Sleeping for 2 minutes")
    time.sleep(120)

    # Check if new pod has come up or not
    command2 = "/usr/local/bin/kubectl get pods -n {0} | grep -i '{1}'".format(ns,key)
    print("Command to check pod status after restart is= ",command2)
    st,output = subprocess.getstatusoutput(command2)
    
    # Check if pod is up or not!
    if st == 0:
        print("New pod has come up checking its status")
        # Parse the output and check if it meets the criteria
        data = output.split()

        if data[1] != "1/1":
            return([data[0],"Container Status is not 1/1 !Check"])
        if data[2] != "Running" :
            return([data[0],"Pod is not in Running Status!Check"])
        else:
            print("Output of new pod meets the criteria.")
            return([data[0],"Pod is OK running from "+data[4]])        
    else:
        print("Pod is not up and running")
        return(["NA","Pod is not up and running! Failed"])
    


#-----------------------------------Caller Logic--------------------------

if __name__ == "__main__":
    checkConsumerLag()

    if  sendMail == True:
        print("Sending mail")
        #mail_to = ["shivalsh@amdocs.com"]
        #mail_from = "DL-ATTCCSOPS@att.com"
        #subject="Alert! Comsumer Lag Check | {}".format(dc_name.upper())
        #mail_send = Mailer
        #m = mail_send.Mailer(mail_to, mail_from)
        #m.sendmail(subject, html_content )
        os.system("mailx -a 'Content-Type: text/html' -s 'Alert! Active Consumer Status Check||{0}' -r {1} {2} < {3}".format(dc_name,FROM,TO,html_file))
        print("Send mail!")
    else:
        print("Everything is OK! No need to send mail")
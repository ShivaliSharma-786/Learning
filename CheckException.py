#!/usr/bin/python3
import subprocess
import sys
import Convertor
import Mailer
import os

#change Directory to script location
scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)
#Declaraions
dc_name=os.uname()[1][1:4].lower()
ns="cgf"
podList=""
# consumerGroup={"streamerName":["consumerName","SSL Excption Status ie T or F","Consume lag ie T or F"]}
consumerGroups={"odf-streamer-pst-daily-streamer":"cgf-ngm-streamer-pst-daily-prod","odf-streamer-pst-subscription":"cgf-ngm-streamer-pst-subscription-prod","odf-streamer-spr":"cgf-ngm-streamer-spr-prod"}
exceptionPods=[]
senMail=False
html_content = "<html><head><title></title></head><body>\n"

# Function to ChEck Exception
def getPods():
    global exceptionPods
    global html_content,senMail
    HeaderDataList=[]
    issue_data_list = []
    sno=0
    #Command to get all pst & spr streamer pods in provisioning ns
    pods=subprocess.getoutput("/usr/local/bin/kubectl get pods -n %s| grep -E 'pst|spr' | awk '{print $1}'" %ns )
    html_content+="</p style=color: red; font-weight: bold;'>javax.net.ssl.SSLException: readHandshakeRecord Found</p><br><br>"
    html_content = html_content + "<table border=\"1\"; width=\"70%\">\n"
    HeaderDataList=["Sno.","PodName","Exception Status"]
    header_record = con.list2html(HeaderDataList, True)
    html_content += header_record
    # loop threw all pods and find Replication Error
    for pod in pods.split('\n'):
        print("Checking logs in pod= ",pod)
        logs=subprocess.getoutput('/usr/local/bin/kubectl logs {0} -n {1}| grep -ir "javax.net.ssl.SSLException: readHandshakeRecord"| sort | uniq'.format(pod,ns))
        print("Value of log is= ",logs)
        count=subprocess.getoutput('/usr/local/bin/kubectl logs {0} -n {1}| grep -ir "javax.net.ssl.SSLException: readHandshakeRecordl"| wc -l'.format(pod,ns))
        print("value of count is =",count)
        #If SSL Exception is found then append details to issue data list
        if int(count) > 0:
            senMail=True
            # True the parameter in consumerGroups dictionary if SSL exception is found!
            for key in consumerGroups.keys:
                 if pod.count(key) > 0:
                    # update the dictionary from False to True
                    issuePod=[pod,consumerGroups[key]]
                    exceptionPods.extend(issuePod)
            issue_data =[sno,pod,"Found"]
            issue_data_list.append(issue_data)
            sno+=1
    print("Issue data list is= ",issue_data_list)
    for issue_record in issue_data_list:
            html_content = html_content + con.list2html(issue_record)
    html_content = html_content + '</table></body></html>'
    print("Find log function ends")

#Function to check the Consumer Lag for pod where SSL Exception was found

               
               
               


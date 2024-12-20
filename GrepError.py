#!/usr/bin/python3
import subprocess
import sys
import Convertor
import Mailer
import os
scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)
dc_name=os.uname()[1][1:4].lower()
senMail=False
html_content = "<html><head><title></title></head><body>\n"
'''
def getLogLevel():
    global html_content,senMail
    cm="sba-profile-manager-logging"
    # Command to check log level of profile manger pods
    st, output = subprocess.getstatusoutput('/usr/local/bin/kubectl describe configmap {0} -n {1} | grep -i "root level"'.format(cm,ns))
    if st !=0:
        print("Configmap not found! Exiting the script")
        html_content+="<p>sba-profile-manager-logging ConfigMap not found! Please Check</p></body></html>\n"
        senMail = True
    else:
        if output.count("ERROR") > 0:
            return True
        else:
            return False
'''

def findLog():
    ns=["provisioning","slc-session","chf-session"]
    global html_content,senMail
    HeaderDataList=[]
    issue_data_list = []
    sno=1
    pods=""
    #Command to get all db pods in provisioning ns
    for n in ns:
        print("Name Space is=",n)
        pods = subprocess.getoutput("/usr/local/bin/kubectl get pods -n %s| grep db-cluster| awk '{print $1}'" %n )
        print("pod list is = ",pods)
        for pod in pods.split('\n'):
            print("Checking logs in pod= ",pod)
            #log=subprocess.getoutput('/usr/local/bin/kubectl logs {0} -n {1}| grep -ir "buffer queue for"| sort | uniq'.format(pod,n))
            #print("Value of log is= ",log)
            #count=subprocess.getoutput('/usr/local/bin/kubectl logs {0} -n {1}| grep -ir "DR consumer buffer queue for PC.* is full"| wc -l'.format(pod,ns))
            ct=subprocess.getoutput('/usr/local/bin/kubectl logs {0} -n {1}| grep -ir "buffer queue for"| wc -l'.format(pod,n))
            count=int(ct.strip())
            print("value of count is =",count,"\n===================")

            #If replication error found then append details to issue data list
            if count > 0:
                senMail=True
                issue_data =[sno,pod,count]
                issue_data_list.append(issue_data)
                sno+=1
    convert = Convertor
    con = convert.Convert()
    html_content+="</p style=color: red; font-weight: bold;'>Replication Error Found: INFO  [DRPartitionBufferReceiver PC*] DRAGENT: DR consumer buffer queue for PC* is full</p><br><br>"
    html_content = html_content + "<table border=\"1\"; width=\"70%\">\n"
    HeaderDataList=["Sno.","PodName","Count"]
    header_record = con.list2html(HeaderDataList, True)
    html_content += header_record
    # loop threw all pods and find Replication Error
    
    print("Issue data list is= ",issue_data_list)
    for issue_record in issue_data_list:
            html_content = html_content + con.list2html(issue_record)
    html_content = html_content + '</table></body></html>'
    print("Find log function ends")



#----------------------------------Function Caller------------------------
findLog()
'''
if res:
    print("Config map Log level is Error! Calling findLog function")
    findLog()
else:
    print("sba-profile-manager-logging Loglevel is not Error! Please Check ")
    html_content+="<p>sba-profile-manager-logging Loglevel is not Error! Please Check</p></body></html>\n"
'''
if  senMail == True:
    print("Inside Send mail")
    mail_to = ["shivalsh@amdocs.com"]
    #mail_to=['SmartOpsATTCCSOPS@amdocs.com','ATTCCSOPS@amdocs.com']
    mail_from = "DL-ATTCCSOPS@att.com"
    subject="Alert!DR consumer buffer queue is full | {}".format(dc_name.upper())
    mail_send = Mailer
    m = mail_send.Mailer(mail_to, mail_from)
    m.sendmail(subject, html_content )
    print("Send mail!")

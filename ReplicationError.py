#!/usr/bin/python3
import subprocess
import sys
import Convertor
import Mailer
import os,re
import yaml
from datetime import datetime,timedelta

scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)
dc_name=os.uname()[1][1:4].lower()
convert = Convertor
con = convert.Convert()

cfg_file='volt_report_config.yaml'.format(dc_name)
if os.path.exists(cfg_file):
    with open(cfg_file) as ym:
        cfg_data = yaml.safe_load(ym)
else:
    print("Config file not present at path")
    sys.exit()
mail_to = ["shivalsh@amdocs.com"]
mail_from = cfg_data['from']
ns_list = cfg_data['ns_list']
#date= (datetime.now() - timedelta(minutes=10)).strftime('%Y-%m-%d %H')
date= datetime.now().strftime('%Y-%m-%d')
print(f'Date Time: {date}')

def findLog():
    issue_data_list = []
    sno,ct=0,0
    html_content = ''
    sendMail = False
    for ns in ns_list:
        print('---------------------------------------------------------')
        print("Name Space is:",ns)
        st, pods = subprocess.getstatusoutput("/usr/local/bin/kubectl get pods -n %s| grep db-cluster| awk '{print $1}'" %ns )
        if st != 0:
            print("Error in getting pods in namespace {ns}! Exiting the script")
            html_content+=f"<p>Error in getting pods! Please Check for NameSpace: {ns}</p></body></html>\n"
            sendMail = True
            continue
        if pods == '':
            print("No pods found in namespace: {0}".format(ns))
            html_content+=f"<p>No pods found in namespace: {ns}</p></body></html>\n"
            sendMail = True
            continue
        for pod in pods.split('\n'):
            #dictioanry to store PC values
            d={}
            # find buffer strings in log
            res=subprocess.getoutput('/usr/local/bin/kubectl logs {0} -n {1}| grep "buffer queue for" | grep "{2}"'.format(pod,ns,date))
            print("\n=================\n",f'Logs grepped in pod {pod} = \n',res,"\n=======================\n\n")
            # Loop threw the logs 
            if res != '':
                for line in res.split('\n'):
                    print("Value of line is= ",line)
                    #find buffer queue full string in logs 
                    match = re.search(r'buffer queue for (PC.*) is full.', line)
                    # if buffer queue full string is found
                    if match:
                        #get partion value
                        partition=match.group(1)
                        print("Partition which is full is= ",partition)
                        # if partion is not in dictionary then add it
                        if partition not in d.keys():
                            d[partition]= True
                        #if partition is in dictionary & is False the again true it
                        elif d[partition]==False:
                            d[partition]= True
                    
                    # if bufffer queue has freed up space then remove the partion from dictionary
                    match2 = re.search(r'buffer queue for (PC.*) has freed up space. DR buffers for this partition will be processed again', line)
                    
                    if match2:
                         #get partion value
                        partition=match2.group(1)
                        print("Partition which is freed is= ",partition)
                        # if partion is in dictionary & is True the again false it
                        if partition in d.keys():
                            d[partition]= False

                
                    now = datetime.now()
                    #print(f"{now}: Checking logs in pod: {pod} and Namespace: {ns}, Number of Error is: {count}")
                    #If replication error found then append details to issue data list
                    print(f"Dictionary for pod {pod}  is = ",d)
            
            if True in d.values():
                sendMail=True
                for key in d.keys():
                    if d[key]==True:
                        ct+=1
                print("value of count is= ",ct)
                issue_data =[sno,ns,pod,ct]
                issue_data_list.append(issue_data)
                sno+=1

    # loop threw all pods and find Replication Error
    
    print("Issue data list is= ",issue_data_list)
    if len(issue_data_list) != 0:
        for issue_record in issue_data_list:
                html_content += con.list2html(issue_record)
    print("Find log function ends")
    return(html_content, sendMail)


#----------------------------------Function Caller------------------------

if __name__ == '__main__':
    html_content ='''<!DOCTYPE html>
        <html>
        <head>
        <title>
        VoltDB Replication Issue
        </title>
        <style>
        th {
        text-align: center; font-size: 12px;
        }
        td {
          text-align: center; font-size: 10px;
        }
        </style>
        </head>
        <body>
    '''
    html_content += "<p style=color: red; font-weight: bold;'>Replication Error Found: Buffer queue is full</p><br><br>"
    html_content = html_content + "<table border=\"1\"; width=\"60%\">\n"
    HeaderDataList=["Sno.","NameSpace","PodName","Count"]
    header_record = con.list2html(HeaderDataList, True)
    html_content += header_record
    html, sendMail = findLog()
    html_content += html
    html_content += '</table></body></html>'
    print("Value of SEND MAIL is= ",sendMail)
    if  sendMail == True:
        print("Inside Send mail")
        subject="Alert! DR consumer buffer queue is full | {}".format(dc_name.upper())
        mail_send = Mailer
        m = mail_send.Mailer(mail_to, mail_from)
        m.sendmail(subject, html_content )
        print("Send mail!")

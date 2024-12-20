#!/usr/bin/python3

import os
import subprocess
import sys
import Convertor
import Mailer
scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)
dc_name=os.uname()[1][1:4].lower()

# get pods name in provisioning ns
ns_list= ['provisioning']
for ns in ns_list:
    pods=subprocess.getoutput("/usr/local/bin/kubectl get pods -n %s| grep db-cluster | awk '{print $1}'" %ns )
    pods=pods.split("\n")
    pod=pods[0]
    print("Choosen pod to login is =",pod)
    query_command="exec @Statistics DRCONSUMER 0;"
    st, output = subprocess.getstatusoutput('/usr/local/bin/kubectl exec %s  -n %s -- sqlcmd  --query="exec @Statistics DRCONSUMER 0;"' %(pod, ns))
    #st,output=subprocess.getstatusoutput('/usr/local/bin/kubectl exec {pod} -n {ns} -- sqlcmd  --query="{query_command}"|grep -Ev "TABLE_NAME|exec|-|\(|^$"'.format(pod=pod,ns=ns,query_command=query_command))
    print("Value od st is= ",st)
    print("Value of output is= ",output)
    if st != 0 :
        print("Issue with command execution")
        sys.exit()
    header=True
    isMail = False
    html_content = ''
    issue_data_list = []
    HeaderDataList=[]
    for line in output.split('\n') :
        print("-------------------------")
        print("Line read is = ",line)
        if line.strip() == '':
            continue
        row = line.strip().split()
        print("Value of row is = ", row)
        if not row[0].startswith('-----') and len(row) in [17, 19]:
            if header == True :
                HeaderData = row
                HeaderDataList = [row[2], row[13]]
                header = False
            else:
                hostname = row[2]
                availableBuffers = ((int(row[15])/1024)/1024)
                print("Value of hostname is =",hostname)
                print("Value of available buffer is = ",availableBuffers)
                if availableBuffers >= 2 and issue_data_list.find(hostname) == -1:
                    issue_data =[hostname,availableBuffers]
                    print("Issue data is ",issue_data)
                    issue_data_list.append(issue_data)
                    isMail = True
    print("Header data is = ",HeaderDataList)
    print("Issue data is ",issue_data_list)
    if isMail == True:
        convert = Convertor
        con = convert.Convert()
        html_content = "<head> <style> th, td { text-align: center; font-size: 12px;} </style> </head>\n"
        html_content = html_content + "<html><table border=\"1\"; width=\"70%\">\n"
        header_record = con.list2html(HeaderDataList, True)
        html_content = html_content + header_record
        for issue_record in issue_data_list:
            html_content = html_content + con.list2html(issue_record)
        html_content = html_content + '</table>'
    else:
        print("All Avaialabele Buffers are OK".format(ns))
if  isMail == True:
    mail_to = ["shivalsh@amdocs.com"]
    mail_from = "DL-ATTCCSOPS@att.com"
    subject="Alert! Avaliable Buffer is less than 80MB {}".format(dc_name)
    import Mailer
    mail_send = Mailer
    m = mail_send.Mailer(mail_to, mail_from)
    m.sendmail(subject, html_content )
    print("Send mail!")
    #os.system("mailx -a 'Content-Type: text/html' -s 'Major alert! Availability Size is >80Mb||{0}-{1}' -r {2} {3} < voltdata.html".format(dc1.upper(), dc2.upper(), mail_from,mail_to))

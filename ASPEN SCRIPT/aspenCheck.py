#!/usr/bin/python3
import subprocess
import sys
import os,re
import yaml
from datetime import datetime,timedelta

scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)

# if config file is not present then exit the script
cfg_file='aspenConfig.yaml'
if os.path.exists(cfg_file):
    with open(cfg_file) as ym:
        cfg_data = yaml.safe_load(ym)
else:
    print("Config file not present at path")
    sys.exit()

#Declarations
outdir=cfg_data['outputdir']
retrydir=cfg_data['retrydir']
errordir=cfg_data['errordir']
processingdir=cfg_data['processingdir']
donedir=cfg_data['donedir']

dc_name=os.uname()[1].split('-')[1].upper()
podname=""
nonDuplicateFiles=[]
today=datetime.now().strftime('%Y%m%d')
today="20240901"

#Function to drop mail
def dropMail(html_content):
    #Declarations
    mail_from = cfg_data['from']
    mail_to = "shivalsh@amdocs.com"
    mail_subject = cfg_data['subject']
    html_file=cfg_data['htmlfile']

    #Drop Mail
    with open(html_file, 'w') as f:
        f.write(html_content)
    os.system("mailx -a 'Content-Type: text/html' -s '{0} || {1} || {2}' -r {3} {4} < {5}".format(mail_subject,dc_name,datetime.now().strftime('%Y-%m-%d'),mail_from,mail_to,html_file))
    print("Mail Sent!")
    sys.exit(0)

#Function to validate file records & fields
def getFileStaus(file,podname):
    numberRecord = subprocess.getoutput("/usr/local/bin/kubectl -n cgf exec -it {0} -- bash -c 'cd {1};cat {2} | head -n -1 | wc -l'".format(podname,outdir,file))
    command = "awk -F '|' '{print NF}'"
    numberField = subprocess.getoutput("/usr/local/bin/kubectl -n cgf exec -it {0} -- bash -c \"cd {1}; cat {2} | head -n -1 | {3} | sort | uniq\"".format(podname, outdir, file, command))
    print("No of record in file {0} is {1}".format(file,numberField))
    if int(numberField) != 9 :
        res="NOT OK"
    else:
        res="OK"
    return [numberRecord,res]

#Function to get null files
def getNullFiles(podname):
    html_content=""
    
    # get null files
    st, res = subprocess.getstatusoutput("/usr/local/bin/kubectl -n cgf exec -it {0} -- bash -c 'find {1} -name 'ASPEN_CCSAU-01-TXT.{2}*null*.txt'| wc -l'".format(podname,outdir,today))
    if st != 0:
        return"<br><br><p>Error in getting null files! Exiting </p><br><br>"

    if res != '0':
        nullfiles = subprocess.getoutput("/usr/local/bin/kubectl -n cgf exec -it {0} -- bash -c 'find {1} -name 'ASPEN_CCSAU-01-TXT.{2}*null*.txt''".format(podname,outdir,today))
        files=[ file.split("/")[-1] for file in nullfiles.split('\n') ]
        sno=0
        
        html_content = html_content + "<br><br><table border=\"1\"; width=\"60%\";align=\"\">\n"
        html_content += "<tr><th colspan=\"6\">Status Of NULL FILES</th></tr>\n"
        html_content += "<tr><th>Sno.</th><th>FILENAME</th><th>TYPE</th><th>Count of FILE Records</th><th>Field Status(9)</th><th>File Status</th></tr>"
        for file in files:
            sno+=1
            typ=file.split('.')[-3]
            res=getFileStaus(file,podname)
            html_content += f"<tr style='color:Red'><td>{sno}</td><td>{file}</td><td>{typ}</td><td>{res[0]}</td><td>{res[1]}</td><td>NOT OK</td></tr>\n"
        html_content += "</table>\n"
        return html_content
    if res == '0':
        return "<br><br><p>No null files found or No Aspen files found</p><br><br>"

#Function to get duplicate & good files
def getDuplicateFiles(podname):
    sno=0
    res=""
    html_content=""
    today=datetime.now().strftime('%Y%m%d')
    today="20240901"
    Duplicates=0
    html_content += "<br><br><table border=\"1\"; width=\"60%\" ;align=\"left\">\n"
    html_content += "<tr><th colspan=\"6\">Status Of Duplicate FILES</th></tr>\n"
    html_content += "<tr><th>Sno.</th><th>FILENAME</th><th>Count of FILE Records</th><th>Field Status(9)</th><th>File Status</th><th>Type</th></tr>"

    #command to get all MON ASPEN FILES
    for typ in ["MON","TTN"]:
        print(f"Checking for file Type is: {type}")
        st, res = subprocess.getstatusoutput("/usr/local/bin/kubectl -n cgf exec -it {0} -- bash -c 'find {1} -name 'ASPEN_CCSAU-01-TXT.{2}*{3}*.txt'| wc -l'".format(podname,outdir,today,typ))
        #print("Value of res is: ",res,"\n")
        if st != 0:
            res+= "<br><br><p>Error in getting ASPEN files! Exiting</p><br><br>"

        if res == '0':
            res+= "<br><br><p>No {} Duplicate Aspen files found </p><br><br>".format(typ)
        if res != '0':
            Duplicates=1
            #Command to get files
            data = subprocess.getoutput("/usr/local/bin/kubectl -n cgf exec -it {0} -- bash -c 'find {1} -name 'ASPEN_CCSAU-01-TXT.{2}*{3}*.txt''".format(podname,outdir,today,typ))
            print("Value of data is",data)
            #Command to seperate files
            files=[file.split("/")[-1] for file in data.split('\n')]
            print("Value of files is: ",files)
            #Commad to get the uniq markets
            markets = set([file.split('.')[-2] for file in files])
            markets=list(markets)
            markets.remove('null')

            #logic to get the file count of same market
            for market in markets:
                print("Chceking for market = ",market)
                matching_files = [file for file in files if market in file]
                print("Files found for {0} are {1}".format(market,matching_files))
                #if count of file is 1 then its a good file
                if len(matching_files) == 1:
                    nonDuplicateFiles.append(matching_files[0])
                #if Count of file is more than 1 then there is duplicate file
                if len(matching_files)>1:
                    sno+=1
                    var=""
                    html_content+="<tr style='color:Red'><td rowspan=\"{0}\">{1}</td>".format(len(matching_files),sno)
                    res=getFileStaus(matching_files[0],podname)
                    print("Value of res is ",res)
                    html_content+="<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td rowspan=\"{5}\">{4}</td></tr>\n".format(matching_files[0],res[0],res[1],"NOT OK",typ,len(matching_files))
                    for i in range(1,len(matching_files)):
                        res1=getFileStaus(matching_files[i],podname)
                        print("Value of res1 is ",res1)
                        html_content+="<tr style='color:Red'><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>\n".format(matching_files[i],res1[0],res1[1],"NOT OK")

    html_content += "</table>\n"
    if Duplicates != 0:
        res=html_content
    return res

#Function to get good file status
def goodFilesStatus(nonDuplicateFiles,podname):
    sno=0
    res=""
    html_content=""
    today=datetime.now().strftime('%Y%m%d')
    today="20240901"
    Duplicates=0
    if not nonDuplicateFiles:
        return "<br><pre>No Non duplicate ASPEN files found</pre>"

    html_content += "<br><br><br><table border=\"1\"; width=\"60%\" ;align=\"left\">\n"
    html_content += "<tr><th colspan=\"6\">Status Of NON-Duplicate FILES</th></tr>\n"
    html_content += "<tr><th>Sno.</th><th>FILENAME</th><th>Count of FILE Records</th><th>Field Status(9)</th><th>File Status</th><th>Type</th></tr>\n"

    for file in nonDuplicateFiles:
        sno +=1
        res=getFileStaus(file,podname)
        html_content += "<tr style='color:Green'><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</t><td>{5}</td></tr>\n".format(sno,file,res[0],res[1],"OK",file.split(".")[-3])

    html_content +="</table>\n"
    return html_content

#Function to get pending files status
# Function to get pending files status
def pendingFilesStatus(podname):
    html_content = ""
    html_content += '<br><br><table border="1" width="60%" align="left">\n'
    html_content += '<tr><th colspan="2">Pending Files Status</th></tr>\n'

    # Files in retry
    retry = subprocess.getoutput('/usr/local/bin/kubectl -n cgf exec -it {0} -- bash -c "ls -1 {1} | wc -l"'.format(podname, retrydir))
    print("Value of retry is =", retry)
    if retry.isdigit() and int(retry) > 0:
        html_content += '<tr><td>Files Pending in Retry</td><td>{}</td></tr>'.format(retry)

    # Files in error
    error = subprocess.getoutput('/usr/local/bin/kubectl -n cgf exec -it {0} -- bash -c "ls -1 {1} | wc -l"'.format(podname, errordir))
    print("Value of error is =", error)
    if error.isdigit() and int(error) > 0:
        html_content += '<tr><td>Files Pending in Error</td><td>{}</td></tr>'.format(error)

    # Files in processing
    processing = subprocess.getoutput('/usr/local/bin/kubectl -n cgf exec -it {0} -- bash -c "ls -1 {1} | wc -l"'.format(podname, processingdir))
    print("Value of processing is =", processing)
    if processing.isdigit() and int(processing) > 0:
        html_content += '<tr><td>Files Pending in Processing</td><td>{}</td></tr></table>'.format(processing)

    return html_content


#Function to get podname processing ASPEN
def getPod():
    # get connect pods name
    processingpod=""
    st,podnames=subprocess.getstatusoutput("/usr/local/bin/kubectl get pods -n cgf| grep 'odf-connect-cluster-connect'| awk '{print $1}'")
    if st != 0:
        return -1
        
    else:
        pods=podnames.split("\n")
        
        for pod in pods:
            print("Checking pod {}".format(pod))
            #command='kubectl -n cgf exec -it {0} -- bash -c "find /tmp/delivery/eom-aspen-sink-httpfile-connector1/ -name ASPEN*{1}*.txt.batch 2> /dev/null" | wc -l'.format(pod,today)
            command = 'kubectl -n cgf exec -it {0} -- bash -c "if [ -d /tmp/delivery/eom-aspen-sink-httpfile-connector1/ ]; then find /tmp/delivery/eom-aspen-sink-httpfile-connector1/ -name \'ASPEN*{1}*.txt.batch\' 2> /dev/null | wc -l; else echo 0; fi"'.format(pod, today)
            st2,count=subprocess.getstatusoutput(command)
            
            if st2 != 0:
                print("Command failed with exit code {}: {}".format(st2, count))
                continue
            else:
                print("Value of count is {0} and type of count is {1}".format(count,type(count)))
                if int(count) > 0:
                    processingpod=pod
    # Return a normal pod & a ASPEN Processing pod
    return [pods[0],processingpod]
            


#----------------------------------Function Caller----------------------------------
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
    # call getPod() to get ASPEn Processing Function
    val=getPod()
    # if unable to fetch podname then drop a mail
    if val[0] == None or val == -1:
        html_content+="<p>Unable to fetch pod processing the ASPEN FILE</p></body></html>"
        print("Unable to fetch pod processing the ASPEN FILE")
        dropMail(html_content)
    podname=val[0]
    print("Pod Processing ASPEN is ",podname)

    html_content += "<h2>ASPEN FILE STATUS REPORT</h2><br><br>"
    html_content += "<p>POD PROCESSING ASPEN FILES IS : {}</p>".format(val[1])

    # call function to check null files
    res = getNullFiles(podname)
    html_content +=  res

    #call function to check duplicates
    res2 = getDuplicateFiles(podname)
    html_content = html_content + "<br><br>" + res2 + "<br><br>"
    
    #call good file function
    print("GOOD Files List is=\n",nonDuplicateFiles)
    res3=goodFilesStatus(nonDuplicateFiles,podname)
    html_content = html_content + "<br><br>" + res3 

    #call pending file function
    """
    if val[1] == "":
        html_content += "<div><br><br><pre style='color:Red'>URGENT: Unble to fetch pod ASPEN processing pod Details</pre></div></body></html>"
    else:
    """
    res4=pendingFilesStatus(podname)
    if res4 != "":
        html_content = html_content + "<br><br>" + res4 + "</body></html>"
    else:
        html_content += "<br><br><pre style='color:Green'>No files stuck in retry, error or processing</pre></body></html>"
    
    dropMail(html_content)

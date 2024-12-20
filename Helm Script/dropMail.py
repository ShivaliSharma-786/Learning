import subprocess
from datetime import datetime, timedelta
import os
import sys
import Convertor
import yaml

# Ensure the script uses the correct working directory
scriptpath = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptpath)

#call this script when comparision is run
# This script will function from OKC & will consolidate the data from GRD & JCS(were helm scrip will run) & will share consolidated mail.


#Config file loads
config_file = os.path.join(scriptpath, 'dc_config.yaml')
with open(config_file) as file:
    dataDict = yaml.load(file, Loader=yaml.FullLoader)

# Email body frame

html_content = ''
html_content = '''<!DOCTYPE html>
        <html>
        <head>
        <title>
        Helm Version Comparison
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
        <body><br>
        '''
data1=subprocess.getoutput('cat /home/nccloud/ccs-prod-common/common/Helm/helmMail.html')
html_content +=data1
html_content += "<br><br>"

#Now ssh to GRD & get the html content file & append it to the mail body
sec=dataDict["SND"][1]
ip=dataDict["SND"][0]
#data2=subprocess.getoutput(f'ssh -q -t {ip} "cat /home/nccloud/ccs-prod-common/common/Helm/helmMail.html"')
data2 = subprocess.getoutput(f'ssh -q -t {ip} "cd home/nccloud/ccs-prod-common/common/Helm/;python3 helmCompare.py && sleep 5 && cat /home/nccloud/ccs-prod-common/common/Helm/helmMail.html"')
html_content +=data2
html_content += "<br><br>"
#Now ssh to ATN & get the html content file & append it to the mail body
sec=dataDict["ATN"][1]
ip=dataDict["ATN"][0]
#data3=subprocess.getoutput(f'ssh -q -t {ip} "cat /home/nccloud/ccs-prod-common/common/Helm/helmMail.html"')
data3 = subprocess.getoutput(f'ssh -q -t {ip} "python3 home/nccloud/ccs-prod-common/common/Helm/helmCompare.py;sleep 5; cat home/nccloud/ccs-prod-common/common/Helm/helmMail.html"')
html_content +=data3
html_content += "<br><br></body></html>\n"

print("html_content is= ",html_content)

#mailing Details
mail_to = ["dl-attccsops@att.com", "attccsops@amdocs.com"]
mail_to = ["shivalsh@amdocs.com"]
mail_from = "DL-ATTCCSOPS@att.com"
subject=f"Consolidated Helm Version Comparison"

import Mailer
mail_send = Mailer
m = mail_send.Mailer(mail_to, mail_from)
m.sendmail(subject, html_content )
print("Send mail!")
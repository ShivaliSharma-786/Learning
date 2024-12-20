#!/usr/bin/python3

import subprocess
from datetime import datetime, timedelta
import os
import sys
import Convertor
import Mailer
import yaml

today = datetime.now().strftime("%Y.%m.%d")
dc_name=os.uname()[1][1:4].upper()
#data Dict
dataDict={"OKC":["166.190.131.10","LTR"],"LTR":["166.190.133.10","OKC"],"GRD":["108.153.37.10","SND"],"SND":["108.154.1.10","GRD"],"JCS":["108.154.177.10","ATN"],"ATN":[" 108.154.87.10","JCS"]}
'''
config_file = 'dc_config.yaml'
with open(config_file) as file:
    dataDict = yaml.load(file, Loader=yaml.FullLoader)
'''
sec=dataDict[dc_name][1]
ip=dataDict[dc_name][0]
print("Secondary is= ", sec)

scriptpath=os.path.dirname(sys.argv[0])

if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)

def splitData(data):
    res=[]
    header = True
    for line in data.strip().split('\n'):
        if header== True:
            header=False
            continue
        line=line.strip().split()
        if "cattle-fleet-system" in line:
            print(line)
            name="fleet-agent"
            ns=line[1]
            index=line[-1].find("+s-")
            chart=line[-1][index+3:]
            version="NA"
        else:
            if len(line) != 10:
                name=line[0]
                ns=line[1]
                chart=line[-1]
                version="NA"
            else:
                name=line[0]
                ns=line[1]
                chart=line[-2]
                version=line[-1]
        d=[name,ns,chart,version]
        res.append(d)
    return res


if __name__=="__main__":
    # Clean up the html file if file exists
    html_file='/home/nccloud/ccs-prod-common/common/Helm/helmMail.html'
    if os.path.exists(html_file):
        with open(html_file, 'w') as file:
            file.truncate(0)
        print(f"{html_file} has been emptied.")

    pri_helm_data = subprocess.getoutput('/usr/local/bin/helm list -A')
    os.system(f'ssh -q -t {ip} "/usr/local/bin/helm list -A" > helm_{sec}.csv')
    print ("Executed")

    sec_helm_data= subprocess.getoutput(f'cat helm_{sec}.csv')

    helm_pri_all=splitData(pri_helm_data)
    helm_sec_all=splitData(sec_helm_data)

    print("Primary data center data is \n")
    print("Primary Helm Data: ", helm_pri_all,"\n\n")
    print("\n------------------------------\nSecondary data center data is\n")
    print("Secondary Helm Data: ", helm_sec_all)

    res=[]
    sno=1
    for lst in helm_pri_all:
        name = lst[0]
        ns = lst[1]
        chart=lst[2]
        ver=lst[3]
        for lst2 in helm_sec_all:
            if name == lst2[0] and ns == lst2[1]:
                if ver != lst2[3] or chart != lst2[2] :
                    l=[sno,name,ns,chart,ver,lst2[2],lst2[3],"NOT OK"]
                    res.append(l)
                else:
                    l=[sno,name,ns,chart,ver,lst2[2],lst2[3],"OK"]
                    res.append(l)
        sno +=1
    print("\n-------------------------------\n","Output List=",res)
    convert = Convertor
    con = convert.Convert()
    html_content = ''
    html_content = html_content + "<table border=\"1\"; width=\"70%\">\n"
    HeaderDataList = ["Sno","Name","Namespace",f"{dc_name} Chart",f"{dc_name} Version",f"{sec} Chart",f"{sec} Version","Status"]
    header_record = con.list2html(HeaderDataList, True)
    html_content = html_content + header_record
    for issue_record in res:
        if issue_record[-1] == "NOT OK":
            html_content = html_content + con.list2html(issue_record,textColor='Red')
        else:
            html_content = html_content + con.list2html(issue_record,textColor='Green')
    html_content = html_content + '</table>'

print("html content is= ",html_content)
open('/home/nccloud/ccs-prod-common/common/Helm/helmMail.html','w').write(html_content)

    

#!/usr/bin/python3
import subprocess
import os
import sys
import datetime
import csv

scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)


y_day=(datetime.datetime.now()-datetime.timedelta(1)).strftime('%Y%m%d')
t_day=(datetime.datetime.now()-datetime.timedelta(0)).strftime('%Y%m%d')
old_day=(datetime.datetime.now()-datetime.timedelta(2)).strftime('%Y%m%d')
configFileStatusCsv_yest=os.path.join(scriptpath,"config_status_"+y_day+".csv")
configFileStatusCsv_tday=os.path.join(scriptpath,"config_status_"+t_day+".csv")
refFileStatusCsv_yest=os.path.join(scriptpath,"ref_status_"+y_day+".csv")
refFileStatusCsv_tday=os.path.join(scriptpath,"ref_status_"+t_day+".csv")


#For Secondary DC GRD/LTR/SND
#--------------------------------------------------------------------------------------------------------------

masterPathmdsum = []
podPathmdsum=[]
dc_name=os.uname()[1][1:4].upper()

#logic to find the md5sum of files at the master node location written here
def getMasterLocation(key,filename,loc):
    #data Dictionary
    if key != "BRMS_To_OC":
        status,md5Sum=subprocess.getstatusoutput('cd {0}; md5sum {1}'.format(loc,filename))
        if status == 0:
            index = md5Sum.find(filename)
            md5Sum = md5Sum[0:index]
            md5Sum = md5Sum.strip()
            lst=[key,filename,md5Sum]
        else:
            lst=[key,filename,'Not Found']

    else:
        #status, name = subprocess.getstatusoutput('cd {0}; find . -maxdepth 1 -type f -mtime -1'.format(loc))
        command = "find . -type f -exec ls -ltr {} + | tail -1 | awk -F \"/\" \'{print $2}\'"
        status, name = subprocess.getstatusoutput('cd {0}; {1}'.format(loc, command))
        if status==0:
            #name=name[2:].strip()
            #BRMS_To_OC_filename = name
            md5Sum=subprocess.getoutput('cd {0}; md5sum {1}'.format(loc,name))
            index = md5Sum.find(name)
            md5Sum = md5Sum[0:index]
            md5Sum = md5Sum.strip()
            lst = [key, name, md5Sum]
        else:
            lst = [key, name, 'Not Found']
    masterPathmdsum.append(lst)


#---------------------------------------------------------------------------------

#logic to find md5sum of pod locations

def getPodmd5sum(podList,key,filename,rsyncLoc,chfLoc,nameSpace,container):
    l = [key, filename]
    print("Pod list inside function ", podList,type(podList))
    for pod in podList:
        # chf,cog, sba-provisioning
        if pod.find('rsyncd')== -1:

            if key == "BRMS_To_TimeNotification" and pod.find("sba-provisioning") != -1:
                command = '/usr/local/bin/kubectl -n {0} exec -it {1} -c {2} -- sh -c "md5sum {3}" 2>/dev/null'.format(
                    'provisioning',pod, 'sba-provisioning','./config/product-config/attc-ref-data/OfferIdToTimeBasedTimers.csv')
                status, md5Sum = subprocess.getstatusoutput('/usr/local/bin/kubectl -n {0} exec -it {1} -c {2} -- sh -c "md5sum {3}" 2>/dev/null'.format('provisioning',pod, 'sba-provisioning','./config/product-config/attc-ref-data/OfferIdToTimeBasedTimers.csv'))

            elif key == "BRMS_To_TimeNotification" and pod.find("chf") != -1:
                status,md5Sum = subprocess.getstatusoutput('/usr/local/bin/kubectl -n {0} exec -it {1} -c {2} -- sh -c "md5sum {3}" 2>/dev/null'.format('ecs',pod,'chf','./config/product-config/attc-ref-data/OfferIdToTimeBasedTimers.csv'))
            else:
                status,md5Sum = subprocess.getstatusoutput(
                    '/usr/local/bin/kubectl -n {0} exec -it {1} -c {2} -- bash -c "md5sum {3}" 2>/dev/null'.format(nameSpace,pod,container,chfLoc))

        #Enter else only if podname is Rsyncd
        else:
            status, md5Sum = subprocess.getstatusoutput(
                     '/usr/local/bin/kubectl -n {0} exec -it {1} -- bash -c "md5sum {2}" 2>/dev/null'.format('configuration',pod,rsyncLoc))

        if status == 0:
            index = md5Sum.find('.')
            md5Sum = md5Sum[0:index]
            md5Sum = md5Sum.strip()
            d = {pod: md5Sum}
            l.append(d)
        else:
            d = {pod: "File not generated"}
            l.append(d)
    podPathmdsum.append(l)

# logic to find md5sum for BRMS
'''
def getPodmd5sumBRMS(podList,key,filename,rsyncLoc,chfLoc,nameSpace,container):
    l = [key, filename]
    print("Pod list inside function ", podList,type(podList))
    for pod in podList:
        if pod.find('rsyncd')== -1:

            if pod.find('chf-76489fbfb')== -1:
                status,md5Sum = subprocess.getstatusoutput('/usr/local/bin/kubectl -n {0} exec -it {1} -c {2} -- bash -c "md5sum {3}" 2>/dev/null'.format(prov
            else:
                status,md5Sum = subprocess.getstatusoutput('/usr/local/bin/kubectl -n {0} exec -it {1} -c {2} -- bash -c "md5sum {3}" 2>/dev/null'.format(ecs,
        else:
            status, md5Sum = subprocess.getstatusoutput(
                     '/usr/local/bin/kubectl -n {0} exec -it {1} -- bash -c "md5sum {2}" 2>/dev/null'.format('configuration',pod,rsyncLoc))
        if status == 0:
            index = md5Sum.find('.')
            md5Sum = md5Sum[0:index]
            md5Sum = md5Sum.strip()
            d = {pod: md5Sum}
            l.append(d)
        else:
            d = {pod: "File not generated"}
            l.append(d)
    podPathmdsum.append(l)
'''

#--------------------------------------------------------------
#function for md5sum comparision bw master node & pod locations

def CompareData(master_mdSum, podList):
    writer.write("<table border=\"1\">\n")
    writer.write("<tr><th colspan=\"2\">Status Of Ref files after distribution by Rsyncd</th></tr>\n")
    writer.write("<tr><th>PodName</th><th>{0}({1})</th>\n".format(podList[0],podList[1]))
    for i in range(2, len(podList)):
        d = podList[i]
        for key in d.keys():
            if d[key] == master_mdSum:
                res="OK"
            else:
                res="NOT OK"
            writer.write("<tr><td>{0}</td><td>{1}</td></tr>\n".format(key,res))
    writer.write("</table>\n")
    writer.write("<br><br>")

#----------------------------------------------------------------------------------

#Code to check the master node location file creation date

def getMasterDate(market,filename,loc):
    
    command1 = "ls -lrth '{}'".format(filename)
    command2 = "awk -F \" \" '{print $6 \" \" $7 \" \" $8}'"
    f = open(loc+filename,'r')
    fline = len(f.readlines())
    print("Value if fline is= ",fline)
    file_stats = os.stat(loc+filename)
    file_size = file_stats.st_size
    f.close()

#converting file size in human readable form -----------------------------
    def sizeof_fmt(size, suffix="B"):
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if abs(size) < 1024.0:
                return f"{size:3.1f}{unit}{suffix}"
            size /= 1024.0
        return f"{size:.1f} Yi{suffix}"

    def get_change(current, previous):
        if current == previous:
            return 0
        try:
            return float(abs(current - previous) / max(previous,current) * 100)
        except ZeroDivisionError:
            return float('inf')



    fsize = sizeof_fmt(file_size , suffix="B")

    status, res = subprocess.getstatusoutput('cd {0};{1} | {2}'.format(loc, command1, command2))
    if status == 0:

        if configFlag == True:
            yestFile = configFileStatusCsv_yest
            csvWriter = config_csv_writer

        elif refFlag == True:
            yestFile = refFileStatusCsv_yest
            csvWriter = ref_csv_writer

        else:
            writer.write("<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td>\n".format(filename, res, fline, fsize))

        with open(yestFile, 'r') as f:
            csv_reader = csv.reader(f)

            yes_count = ""
            for lines in csv_reader:
                if lines[0] == filename:
                    yes_count = lines[2]
                    print("value of yes_count ie File Count is = ",yes_count)
                elif lines[0].startswith("OC") and lines[0].endswith(".xml") and filename.startswith(
                        "OC") and filename.endswith(".xml"):
                    yes_count = lines[2]

        csvWriter.writerow([filename, res, fline, fsize])

        deviation = get_change(int(fline), int(yes_count))
        if deviation >= 5:
            writer.write("<tr style='color:Red'>\n")
        else:
            writer.write("<tr>")

        writer.write("<td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4:.2f}%</td><td>{5}</td>\n".format(filename, res, fline,yes_count, deviation,fsize))

    else:
        writer.write("<tr><td>{0}</td><td>{1}</td>\n".format(filename, "File NOT FOUND"))
    writer.write("</tr>\n")

#-------------------------Driver Code for Master Node md5sum-----------------------

refDict = {"TLG_To_Roaming_Zone": ["LocationZoneTable.csv","/home/nccloud/ccs-ref-config-data/config-data/chf/product-config/rzd/"],
           "SGW_IP_To_PLMN": ["SgwIpToPlmnTable.csv","/home/nccloud/ccs-ref-config-data/config-data/chf/product-config/attc-ref-data/"],
           "RMS_To_Serving_SID": ["PlmnServingSidTable.csv","/home/nccloud/ccs-ref-config-data/config-data/chf/product-config/attc-ref-data/"],
           "Market_To_Timezone": ["MarketToTimeZoneTable.csv","/home/nccloud/ccs-ref-config-data/config-data/cog/product-config/attc-ref-data/"],
           "BRMS_To_TimeNotification": ["OfferIdToTimeBasedTimers.csv","/home/nccloud/ccs-ref-config-data/config-data/cog/product-config/attc-ref-data/"],
           "BRMS_To_OC": ["File not generated","/home/nccloud/ccs-ref-config-data/config-data/ocrt/product-config/offercatalog/config/"]}



#-----------------------------------------------------------------------------------------------
for key in refDict.keys():
    getMasterLocation(key,refDict[key][0],refDict[key][1])

print("Master path md5sum",masterPathmdsum,"\n")

#------------------------Driver Code for md5sum of pod locations--------------------------------------------

podLocationDict={"TLG_To_Roaming_Zone":{"fileName":"LocationZoneTable.csv","Rsynd":"./source_data/chf/product-config/rzd/LocationZoneTable.csv","CHF":"./config/product-config/rzd/LocationZoneTable.csv"},
"SGW_IP_To_PLMN":{"fileName":"SgwIpToPlmnTable.csv","Rsynd":"./source_data/chf/product-config/attc-ref-data/SgwIpToPlmnTable.csv","CHF":"./config/product-config/attc-ref-data/SgwIpToPlmnTable.csv"},
"RMS_To_Serving_SID":{"fileName":"PlmnServingSidTable.csv","Rsynd":"./source_data/chf/product-config/attc-ref-data/PlmnServingSidTable.csv","CHF":"./config/product-config/attc-ref-data/PlmnServingSidTable.csv"},
"Market_To_Timezone":{"fileName":"MarketToTimeZoneTable.csv","Rsynd":"./source_data/cog/product-config/attc-ref-data/MarketToTimeZoneTable.csv","CHF":"./opt/deploy/SBA/config/product-config/attc-ref-data/MarketToTimeZoneTable.csv"},
"BRMS_To_TimeNotification":{"fileName":"OfferIdToTimeBasedTimers.csv","Rsynd":"./source_data/cog/product-config/attc-ref-data/OfferIdToTimeBasedTimers.csv","CHF":"./opt/deploy/SBA/config/product-config/attc-ref-data/OfferIdToTimeBasedTimers.csv"},
                 "BRMS_To_OC":{"fileName":"File not generated","Rsynd":"./source_data/ocrt/product-config/offercatalog/config/","CHF":"./config/product-config/offercatalog/config/"}}

RsyncPod=subprocess.getoutput("/usr/local/bin/kubectl get pods -n configuration | grep 'rsyncd' | grep -v dashboard | awk '{print $1}'| sort -ur")
print("RsyncD pod Name",RsyncPod)

for key in podLocationDict.keys():
    if key in ["TLG_To_Roaming_Zone", "SGW_IP_To_PLMN", "RMS_To_Serving_SID"]:
        podList=subprocess.getoutput("/usr/local/bin/kubectl get pods -n ecs | grep 'chf' | grep -v dashboard | awk '{print $1}'| sort -ur")
        #print(podList)
        podList+="\n"
        podList+=RsyncPod
        #print(podList)
        podList = podList.split('\n')
        print("TLG_To_Roaming_Zone,SGW_IP_To_PLMN & RMS_To_Serving_SID pod list= ",podList)
        getPodmd5sum(podList,key,podLocationDict[key]["fileName"],podLocationDict[key]["Rsynd"],podLocationDict[key]["CHF"],'ecs','chf')

    elif key == "Market_To_Timezone":
        podList = subprocess.getoutput(
            "/usr/local/bin/kubectl get pods -n provisioning | grep 'custom-provisioning-gateway' | awk '{print $1}'| sort -ur")
        #print(podList)
        podList+="\n"
        podList+=RsyncPod
        print("Market_To_Timezone pod list= ",podList)
        podList = podList.split('\n')
        getPodmd5sum(podList, key, podLocationDict[key]["fileName"], podLocationDict[key]["Rsynd"],
                     podLocationDict[key]["CHF"],'provisioning','custom-provisioning-gateway')

    elif key == "BRMS_To_TimeNotification":
        podList = []
        podList1 = subprocess.getoutput(
            "/usr/local/bin/kubectl get pods -n provisioning | grep -E 'custom-provisioning-gateway|sba-provisioning' | awk '{print $1}'| sort -ur")
        podList1+="\n"
        podList1+=RsyncPod
        podList2 = subprocess.getoutput("/usr/local/bin/kubectl get pods -n ecs | grep 'chf' | grep -v dashboard | awk '{print $1}'| sort -ur")
        podList1 = podList1.split('\n')
        podList2 = podList2.split('\n')
        podList = podList1 + podList2
        print("final pod list below ",podList)
        getPodmd5sum(podList, key, podLocationDict[key]["fileName"], podLocationDict[key]["Rsynd"],podLocationDict[key]["CHF"],'provisioning','custom-provisioning-gateway')

    else:
        podList = subprocess.getoutput(
            "/usr/local/bin/kubectl get pods -n offers | grep 'offer-catalog-sba' | awk '{print $1}'| sort -ur")
        #print(podList)
        podList+="\n"
        podList+=RsyncPod
        print("BRMS_TO_OC pod list= ",podList)
        podList = podList.split('\n')

        #Find latest name of the oc file from master node loc
        command = "find . -type f -exec ls -ltr {} + | tail -1 | awk -F \"/\" \'{print $2}\'"
        status, BRMS_To_OC_filename = subprocess.getstatusoutput(
            'cd /home/nccloud/ccs-ref-config-data/config-data/ocrt/product-config/offercatalog/config/; {}'.format(command))
        #status, BRMS_To_OC_filename = subprocess.getstatusoutput('cd /home/nccloud/CHF/ECS8.6.0/config-data/ocrt/product-config/offercatalog/config/; find .
        if status == 0:
            #BRMS_To_OC_filename = BRMS_To_OC_filename[2:].strip()
            podLocationDict[key]["fileName"]=BRMS_To_OC_filename
            podLocationDict[key]["Rsynd"] +=BRMS_To_OC_filename
            podLocationDict[key]["CHF"] +=BRMS_To_OC_filename
        getPodmd5sum(podList, key, podLocationDict[key]["fileName"], podLocationDict[key]["Rsynd"],
                     podLocationDict[key]["CHF"],'offers','ocrt')


#------------------------------Logic for Comparision bw Master Node & Pod Location-----------------

#Dates
Current_Date = datetime.datetime.today().strftime("%Y%m%d")
Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
Previous_Date = Previous_Date.strftime("%Y%m%d")

#Email File
html_file='mail_alert_file.html'
FROM="DL-ATTCCSOPS@att.com"
#TO="urvik@amdocs.com"
#TO="shivalsh@amdocs.com shivam.kapoor@amdocs.com saurabh.sharma@amdocs.com"
TO="SmartOpsATTCCSOPS@amdocs.com attccsops@amdocs.com DL-ATTCCSOPS@att.com"

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
writer.write("<h3>Ref Files Status || {0} || {1}</h3>\n".format(dc_name,Current_Date))

ConfigDict =  {"Disaster_Area_Config":["DisasterAreaConfigTable.csv","/home/nccloud/ccs-ref-config-data/config-data/chf/product-config/attc-ref-data/"],
           "Private_Routing":["PrivateRoutingDNN.csv","/home/nccloud/ccs-ref-config-data/config-data/chf/product-config/attc-ref-data/"],
           "Chf_Group_VIP":["CHFGroupIDToVIP.csv","/home/nccloud/ccs-ref-config-data/config-data/cog/product-config/attc-ref-data/"],
           "Chf_Dimension_ChfGroupID":["CHFDimensionIDToCHFGroupID.csv","/home/nccloud/ccs-ref-config-data/config-data/cog/product-config/attc-ref-data/"],
           "Account_Type":["AccountTypeSubTypeToCHFDimensionID.csv","/home/nccloud/ccs-ref-config-data/config-data/cog/product-config/attc-ref-data/"],
           "General_config_Items":["GeneralConfigItems.csv","/home/nccloud/ccs-ref-config-data/config-data/chf/product-config/attc-ref-data/"]}

#-------------------------------------Logic to find last updated date of Config Files--------

writer.write("<br><br>")
writer.write("<table border=\"1\">\n")
writer.write("<tr><th colspan=\"6\">Status Of Config Files</th></tr>\n")
writer.write("<tr><td>File Name</td><td>Last Update</td><td>No of rows</td><td>Yesterday count</td><td>Deviation</td><td>File Size</td></tr>\n")

configFlag=True

configCsv=open(configFileStatusCsv_tday,'w+')
config_csv_writer = csv.writer(configCsv)

for key in ConfigDict.keys():
    getMasterDate(key, ConfigDict[key][0], ConfigDict[key][1])
writer.write("</table>\n")
writer.write("<br><br>\n")

configCsv.close()

file_check=os.path.isfile(os.path.join(scriptpath,"config_status_"+old_day+".csv"))
if file_check == True:
    os.remove(os.path.join(scriptpath,"config_status_"+old_day+".csv"))

configFlag=False

#-------------------------------------Logic to find last updated date of file at master Node location--------
writer.write("<br><br>")
writer.write("<table border=\"1\">\n")
writer.write("<tr><th colspan=\"6\">Status Of Ref files in Master Node</th></tr>\n")
writer.write("<tr><td>File Name</td><td>Last Update</td><td>No of Rows</td><td>Yesterday Count</td><td>Deviation</td><td>File Size</td></tr>\n")

refFlag=True
refCsv=open(refFileStatusCsv_tday,'w+')
ref_csv_writer = csv.writer(refCsv)

for key in refDict.keys():
    if key == "BRMS_To_OC":
        command = "find . -type f -exec ls -ltr {} + | tail -1 | awk -F \"/\" \'{print $2}\'"
        status,filename=subprocess.getstatusoutput('cd {0};{1}'.format(refDict[key][1],command))
        print("\n Oc.xml latest file= ",filename,"\n")
        getMasterDate(key, filename, refDict[key][1])
    else:
        getMasterDate(key, refDict[key][0], refDict[key][1])
writer.write("</table>\n")
writer.write("<br><br>\n")

file_check=os.path.isfile(os.path.join(scriptpath,"ref_status_"+old_day+".csv"))
if file_check == True:
    os.remove(os.path.join(scriptpath,"ref_status_"+old_day+".csv"))

refCsv.close()
refFlag=False

#-------------------------------Logic for Master Node file Comparision with pods-------------

for i in range(len(masterPathmdsum)):
    print("Market Name= ",masterPathmdsum[i][0])
    print("Master Node md5sum =",masterPathmdsum[i][2])
    print("pod list= ",podPathmdsum[i])
    CompareData(masterPathmdsum[i][2],podPathmdsum[i])



writer.write("</html>\n")
writer.close()
os.system("mailx -a 'Content-Type: text/html' -s 'Ref File Status||{0}' -r {1} {2} < {3}".format(dc_name,FROM,TO,html_file))
print("Mail Sent!")

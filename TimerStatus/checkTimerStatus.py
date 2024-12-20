#!/usr/bin/python3
import csv
import subprocess
import os
import sys
import datetime
import timerConfig 

scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)

#Declartions
html_file='timerStatus.html'
dc_name=os.uname()[1][1:4].upper()
today=(datetime.datetime.now()-datetime.timedelta(0)).strftime('%Y-%m-%d')
threshold=timerConfig.threshold
# Dynamically get the cluster value based on dc_name
cluster_attr = f"{dc_name}_Cluster"
cluster = getattr(timerConfig, cluster_attr, None)

#Threshold Trend  Report
Trendreport=dc_name +'_'+ today + '.csv'

#Get pod name
def getPod():
    #Get the pod status
    pod_name = subprocess.getoutput("/usr/local/bin/kubectl get pods -n provisioning | grep 'profile-manager-db-cluster' | awk -F ' ' '{print $1}' | head -1")
    return pod_name

#Get Timer Count
def getTimerStatus(pod_name):
    command = '/usr/local/bin/kubectl exec -i {0} -n provisioning -- sqlcmd --query="select count(1) from VOLTDBPROFILEMANAGER_TIMER where LAST_ACTIVE_CLUSTER_ID=\'{1}\' and timer_value < NOW ;"'.format(pod_name, cluster)
    #command='kubectl exec -it {} -n provisioning -- sqlcmd --query="select count(1) from VOLTDBPROFILEMANAGER_TIMER where timer_value < NOW ;"'.format(pod_name)
    res = subprocess.getoutput(command)
    print(res)
    count= res.split('\n')[4]
    #store timer count in a file
    current_time= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(Trendreport, 'a') as f:
        f.write(f"{current_time},{count}\n")
        f.close()
    return res,count

#add logic to remove files older than 10 days
def delete_old_files(directory, days=10):
    import time
    now = time.time()
    cutoff = now - (days * 86400)

    for filename in os.listdir(directory):
        if filename.startswith(dc_name+"_") and filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                file_modified = os.path.getmtime(filepath)
                if file_modified < cutoff:
                    os.remove(filepath)
                    print(f"Deleted old file: {filepath}")

if __name__ == '__main__':
    # Clean up the html file if file exists & is non
    '''
    if os.path.exists(html_file):
        with open(html_file, 'w') as file:
            file.truncate(0)
        print(f"{html_file} has been emptied.")
    '''
    
    # get podname
    pod_name = getPod()

    #get timer status
    res,count=getTimerStatus(pod_name)

    if int(count) > int(threshold):
        #Write the output to html file
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
        writer.write("<h3>Profile Manager Timer Status || {0} || {1}</h3>\n".format(dc_name,today))
        writer.write("<p>The timer Count is <b>{}</b></p>".format(count))
        writer.write("<p>{}</p>".format(res))
        writer.write("<br><h3>Timer Trend </h3><br>")
        #Check if the trend file exists & is non-empty!
        if os.path.exists(Trendreport) and os.path.getsize(Trendreport) > 0:
            # if file exists then read the threshold csv line by line & separate the value of time & count. Also highlight the count in red if it's increasing & add a % deviation column
            with open(Trendreport, 'r') as f:
                reader = csv.reader(f)
                writer.write("<table border='1'>")
                writer.write("<tr><th>Time</th><th>Count</th><th>Status</th><th>% Deviation</th></tr>")
                
                previous_count = None
                
                for row in reader:
                    time = row[0]
                    count = int(row[1])
                    writer.write("<tr>")
                    writer.write("<td>{}</td>".format(time))
                    
                    # Calculate % deviation
                    if previous_count is not None:
                        if previous_count == 0:
                            deviation = 0
                        else:
                            deviation = round(((count - previous_count) / previous_count) * 100, 2)
                    else:
                        deviation = 0
                    
                    # Highlight count in red if it's >500
                    if int(count) > int(threshold):
                        writer.write("<td style='color:red;'>{}</td>".format(str(count)))
                        Status = "NOT OK""
                        writer.write("<td style='color:red;'>{}</td>".format(Status))
                    else:
                        writer.write("<td>{}</td>".format(str(count)))
                        Status = "OK"
                        writer.write("<td>{}</td>".format(Status))
                    writer.write("<td>{}</td>".format(str(deviation)+"%"))
                    writer.write("</tr>\n")
                    
                    previous_count = count
                
                writer.write("</table>")
                                
        else:
            writer.write("Alert!The trend file does not exist or is empty! in {}".format(dc_name))  
        writer.close()

        # Call the function to delete files older than 10 days
        scriptpath=os.getcwd()
        delete_old_files(scriptpath)


        #Email File
        FROM="DL-ATTCCSOPS@att.com"
        #TO="shivalsh@amdocs.com "
        #TO="shivalsh@amdocs.com shivam.kapoor@amdocs.com saurabh.sharma@amdocs.com"
        TO="SmartOpsATTCCSOPS@amdocs.com attccsops@amdocs.com DL-ATTCCSOPS@att.com"
        os.system("mailx -a 'Content-Type: text/html' -s 'Timer Status | {0}' -r {1} {2} < {3}".format(dc_name,FROM,TO,html_file))
        print("Mail Sent!")       
    else:
        print(res)
        print("Timer Status is OK")

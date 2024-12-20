#!/usr/bin/python3
import csv
import subprocess
import os
import sys
import datetime
import CleanupConfig 
import re
scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)

#Declartions
html_file='CleanupStatus.html'
dc_name=os.uname()[1][1:4].upper()
current_date=(datetime.datetime.now()-datetime.timedelta(0)).strftime('%Y-%m-%d')
job = CleanupConfig.Jobname
pattern = CleanupConfig.LogString
#Get Job name
def getJob():
    #Get the pod status
    print("Checking for job= ",job)
    job_name = subprocess.getoutput("/usr/local/bin/kubectl get pods -n provisioning | grep 'cleanupexpiredsubscribers' | awk -F ' ' '{print $1}'")
    job_name=job_name.split("\n")
    return job_name

#Get logs
def getJobLogs(job_name,pattern):
    print("Search String is ",pattern)
    command = f"/usr/local/bin/kubectl logs -c cleanupexpiredsubscribers-housekeeping-container {job_name} -n provisioning"
    res = subprocess.getoutput(command)
    match = re.search(pattern,res)
    if match:
        # Now get expired Subs count
        Count = int(match.group(1))
        print(f"Deleted {Count} expired subscribers")
        return Count
    else:
        return"No Expired Subscribers found"
    
    

if __name__ == '__main__':
    # get jobname
    job_name = getJob()
    print("Checking in pod = ",job_name)

    #get logs
    for pod in job_name:
        print("Checking pattern in pod = ",pod)
        Count=getJobLogs(pod,pattern)
        print(f"Subs count in {pod} is {Count}")

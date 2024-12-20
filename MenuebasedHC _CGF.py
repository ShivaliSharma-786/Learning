#!/usr/bin/python3
import subprocess
import sys,os
scriptpath=os.path.dirname(sys.argv[0])
if scriptpath== '':
    scriptpath='./'
os.chdir(scriptpath)

def checkPod():
    st, pods = subprocess.getstatusoutput("/usr/local/bin/kubectl get pods -A| grep -Ev '1/1|2/2|3/3|4/4|5/5|Completed'")
    if st != 0:
        print("Error in getting pods Status!")
    else:
        print("Pod Status is = \n",pods)

def checkNode():
    st, nodes = subprocess.getstatusoutput("/usr/local/bin/kubectl get nodes")
    if st != 0:
        print("Error in getting nodes Status!")
    else:
        print("Node Status is = \n",nodes)

def checkTopNode():
    st, top = subprocess.getstatusoutput("/usr/local/bin/kubectl top node")
    if st != 0:
        print("Error in getting top Node Status!")
    else:
        print("Top Node Status is = \n",top)

def checkSvc():
    st, svc = subprocess.getstatusoutput("/usr/local/bin/kubectl get svc -A")
    if st != 0:
        print("Error in getting svc Status!")
    else:
        print("Svc Status is = \n",svc)


def checkElasticHealth():
    st, elastic = subprocess.getstatusoutput("/usr/local/bin/kubectl get elastic -n ads")
    if st != 0:
        print("Error in getting Elastic Health Status!")
    else:
        print("Elastic Health Status is = \n",elastic)

def checkKibana():
    st, kibana = subprocess.getstatusoutput("cd /home/azureuser/workdir/ccscgfeastus2prodstfs001-prod-01/Automation/Common_CGF/Kibana;./get_kibana_timestamp.sh")
    if st != 0:
        print("Error in getting Kibana Status!")
    else:
        print("Kibana Status is = \n NOTE: Mail will be dropped if any issue is observed!",kibana)

def checkZombiePod():
    st, zombie = subprocess.getstatusoutput("cd /home/azureuser/workdir/ccscgfeastus2prodstfs001-prod-01/Automation/Common_CGF/consul_status/; ./zombie_find_consul.sh")
    if st != 0:
        print("Error in getting Zombie Pod Status!")
    else:
        print("Zombie Pod Status is = \n",zombie,"\n NOTE: Mail will be dropped if any issue is observed!")


def checkUQConnectivity():
    st, uq = subprocess.getstatusoutput("cd /home/azureuser/workdir/ccscgfeastus2prodstfs001-prod-01/Automation/Common_CGF/UQAlert/ ; ./CheckUQ.sh ")
    if st != 0:
        print("Error in getting UQ Connectivity Status!")
    else:
        print("UQ Connectivity Status is = \n NOTE: Mail will be dropped if any issue is observed!",uq)

def checkLicenseCheck():
    st, license = subprocess.getstatusoutput("cd /home/azureuser/workdir/ccscgfeastus2prodstfs001-prod-01/Automation/Common_CGF/CheckLicense/ ; ./License_Check.sh")
    if st != 0:
        print("Error in getting License Check Status!")
    else:
        print("Status will be shared over mail")

def checkPVC():
    st, pvc = subprocess.getstatusoutput("cd /home/azureuser/workdir/ccscgfeastus2prodstfs001-prod-01/Automation/Common_CGF/infra_alerts/ ; ./mountPoints.py")
    if st != 0:
        print("Error in getting PVC Status!")
    else:
        print("PVC Status will be shared over mail")

def checkConnectorStatus():
    st, connector = subprocess.getstatusoutput("cd /home/azureuser/; ./get_connectors.sh")
    if st != 0:
        print("Error in getting Connector Status!")
    else:
        print("Connector Status is = \n",connector)


if __name__ == '__main__':
    option=True
    while option:
        print("Enter 1 check pod status")
        print("Enter 2 to  check Node status")
        print("Enter 3 to check top node status")
        print("Enter 4 to check services svc status")
        print("Enter 5 to check the elastic health Status")
        print("Enter 6 to check the latest hit in kibana")
        print("Enter 7 to check the Zombie pod status")
        print("Enter 8 to chcek UQ Connectivity")
        print("Enter 9 to check License Check")
        print("Enter 10 to check the mount point status")
        print("Enter 11 for Connector Status")
        print("Enter 12 to exit")
        option=int(input("Enter you choice: "))
        if option==12:
            print("Existing the Script")
            exit(0)
        elif option==1:
            checkPod()
        elif option==2:
            checkNode()
        elif option==3:
            checkTopNode()
        elif option==4:
            checkSvc()
        elif option==5:
            checkElasticHealth()
        elif option==6:
            checkKibana()
        elif option==7:
            checkZombiePod()
        elif option==8:
            checkUQConnectivity()
        elif option==9:
            checkLicenseCheck()
        elif option==10:
            checkPVC()
        elif option==11:
            checkConnectorStatus()
        else:
            print("Invalid Option! Please select the correct option")
            continue

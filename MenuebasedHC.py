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

def checkNRF():
    st, nrf = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/chf-only/NRF/; ./RegistrationCheck.sh")
    if st != 0:
        print("Error in getting NRF Status!")
    else:
        print("NRF Status is = \n",nrf)

def checkECS():
    st, ecs = subprocess.getstatusoutput("/usr/local/bin/kubectl get pods -n ecs | wc -l")
    if st != 0:
        print("Error in getting ECS Status!")
    else:
        print("ECS Status is = \n",ecs) 

def checkCHFSession():
    st, chf = subprocess.getstatusoutput("/usr/local/bin/kubectl get pods -n chf-session | wc -l")
    if st != 0:
        print("Error in getting CHF Status!")
    else:
        print("CHF Status is = \n",chf)

def checkSLCSession():
    st, slc = subprocess.getstatusoutput("/usr/local/bin/kubectl get pods -n slc-session | wc -l")
    if st != 0:
        print("Error in getting SLC Status!")
    else:
        print("SLC Status is = \n",slc)

def checkProvisioning():
    st, prov = subprocess.getstatusoutput("/usr/local/bin/kubectl get pods -n provisioning | wc -l")
    if st != 0:
        print("Error in getting Provisioning Status!")
    else:
        print("Provisioning Status is = \n",prov)

def checkElasticHealth():
    st, elastic = subprocess.getstatusoutput("/usr/local/bin/kubectl get elastic -n monitoring")
    if st != 0:
        print("Error in getting Elastic Health Status!")
    else:
        print("Elastic Health Status is = \n",elastic)

def checkKibana():  
    st, kibana = subprocess.getstatusoutput("cd ~/ccs-prod-common/common/Kibana/;./get_kibana_timestamp.sh")
    if st != 0:
        print("Error in getting Kibana Status!")
    else:
        print("Kibana Status is = \n",kibana)

def checkUserSanity():
    st, user = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/chf-only/Sanity_Utility/Provision_user/ ; ./user_sanity.sh")
    if st != 0:
        print("Error in getting User Sanity Status!")
    else:
        print("Status will be shared on e-mail in sometime")

def checkCRDProcessing():
    st, crd = subprocess.getstatusoutput("/usr/bin/python3 /home/nccloud/ccs-prod-common/chf-only/CheckCDRs/CheckUnprocessedCDR.py")
    if st != 0:
        print("Error in getting CRD Processing Status!")
    else:
        print("CRD Processing Status is = \n",crd)

def checkZombiePod():
    st, zombie = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/common/consul_status/; ./zombie_find_consul.sh")
    if st != 0:
        print("Error in getting Zombie Pod Status!")
    else:
        print("Zombie Pod Status is = \n",zombie,"\n Mail will be dropped if any zombie pod is found")

def checkTelnetConnectivity():
    st, telnet = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/chf-only/Connectivity/; ./Telnet.shh")
    if st != 0:
        print("Error in getting Telnet Connectivity Status!")
    else:
        print("Telnet Connectivity Status is = \n",telnet)

def checkUQConnectivity():
    st, uq = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/common/UQAlert/ ; ./CheckUQ.sh ")
    if st != 0:
        print("Error in getting UQ Connectivity Status!")
    else:
        print("UQ Connectivity Status is = \n",uq)

def checkLicenseCheck():
    st, license = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/common/CheckLicense/ ; ./License_Check.sh")
    if st != 0:
        print("Error in getting License Check Status!")
    else:
        print("License Check Status is = \n",license)

def checkMountPoint():
    st, mount = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/chf-only/mountpoints ; /usr/bin/python3 Config_Mount.py; /usr/bin/python3 mountPoints.py")
    if st != 0:
        print("Error in getting Mount Point Status!")
    else:
        print("Mount Point Status is = \n",mount,"\n mail will be dropped in case of any issue is observed with mount points")

def checkS1C1Process():
    st, s1c1 = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/common/check_service_status/ ; ./s1pc1.sh")
    if st != 0:
        print("Error in getting S1C1 Process Status!")
    else:
        print("S1C1 Process Status is = \n",s1c1)

def checkDockerConnectivity():
    st, docker = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/common/check_service_status ; ./Docker_Mon.sh")
    if st != 0:
        print("Error in getting Docker Connectivity Status!")
    else:
        print("Docker Connectivity Status is = \n",docker)

def checkNTPConnectivity():
    st, ntp = subprocess.getstatusoutput("cd /home/nccloud/ccs-prod-common/common/check_service_status/ ; ./NTP_Mon.sh")
    if st != 0:
        print("Error in getting NTP Connectivity Status!")
    else:
        print("NTP Connectivity Status is = \n",ntp)



if __name__ == '__main__':
    option=True
    while option:
        option=int(input('''Enter 1 check pod status\n 
                        Enter 2 to  check Node status\n 
                        Enter 3 to check top node status\n 
                        Enter 4 to check services svc status\n
                        Enter 5 to check NRF status\n
                        Enter 6 to check count of pods in ECS Namespace\n
                        Enter 7 to check the count of pods in chf-session Namespace\n
                        Enter 8 to check the count of pods in slc-session Namespace\n
                        Enter 9 to check the count of pods in provisioning\n
                        Enter 10 to check the elastic health Status\n
                        Enter 11 to check the latest hit in kibana\n
                        Enter 12 to do user sanity\n
                        Enter 13 to check the CRD Processing status
                        Enter 14 to check the Zombie pod status
                        Enter 15 to check the Telnet Connectivity Status\n
                        Enter 16 to chcek UQ Connectivity\n
                        Enter 17 to check License Checkk\n
                        Enter 18 to check the mount point status\n
                        Enter 19 to check S1C1 Process Status\n
                        Enter 20 to check Docker Connectivity  Check\n
                        Enter 21 to check NTP Connectivity Check\n
                        Enter 22 to exit\n '''))
        if option==22:
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
            checkNRF()
        elif option==6:
            checkECS()
        elif option==7:
            checkCHFSession
        elif option==8:
            checkSLCSession()
        elif option==9:
            checkProvisioning()
        elif option==10:
            checkElasticHealth()
        elif option==11:
            checkKibana()
        elif option==12:
            checkUserSanity()
        elif option==13:
            checkCRDProcessing()
        elif option==14:
            checkZombiePod()
        elif option==15:
            checkTelnetConnectivity()
        elif option==16:
            checkUQConnectivity()
        elif option==17:
            checkLicenseCheck()
        elif option==18:
            checkMountPoint()
        elif option==19:
            checkS1C1Process()
        elif option==20:
            checkDockerConnectivity()
        elif option==21:
            checkNTPConnectivity()
        else:
            print("Invalid Option! Please select the correct option")
            continue

            

    
    
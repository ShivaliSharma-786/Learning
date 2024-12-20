#!/usr/bin/python3

import re
import glob
import csv
import subprocess
from datetime import datetime, timedelta

#pattern1 = 2024-08-30 09:36:49,583 [vert.x-eventloop-thread-6] ERROR c.o.c.m.s.ChargingdataApiHandler - transactionId=35208c42-e0d0-4bc8-8d2f-a6ec8fa29250, subscriberId=imsi-310280109505161 - postChargingData - HTTP/2 - request that caused the error = [accept=*/*, content-type=application/json, x-forwarded-proto=http, x-request-id=35208c42-e0d0-4bc8-8d2f-a6ec8fa29250, x-envoy-expected-rq-timeout-ms=30000, content-length=1730] - body = [{"invocationSequenceNumber":0,"invocationTimeStamp":"2024-08-30T09:36:49Z","multipleUnitUsage":[{"ratingGroup":101,"requestedUnit":{}},{"ratingGroup":102}],"nfConsumerIdentification":{"nFFqdn":"smf01.shp1a.shp.smf.5gc.mnc410.mcc310.3gppnetwork.org","nFIPv4Address":"108.150.5.14","nFName":"a1b2c3d4-dddd-0006-abcd-1a2b3c4d5e6f","nFPLMNID":{"mcc":"310","mnc":"280"},"nodeFunctionality":"SMF"},"notifyUri":"http://108.150.5.14/nsmf-convergedcharging/v2/941543/notify","pDUSessionChargingInformation":{"chargingId":941543,"pduSessionInformation":{"authorizedQoSInformation":{"5qi":8,"arp":{"preemptCap":"NOT_PREEMPT","preemptVuln":"PREEMPTABLE","priorityLevel":12}},"authorizedSessionAMBR":{"downlink":"10000000000 bps","uplink":"10000000000 bps"},"chargingCharacteristics":"0000","chargingCharacteristicsSelectionMode":"HOME_DEFAULT","dnnId":"nrphone.mnc410.mcc310.gprs","hPlmnId":{"mcc":"310","mnc":"410"},"networkSlicingInfo":{"sNSSAI":{"sst":1}},"pduAddress":{"pduIPv4Address":"10.155.21.183","pduIPv6AddresswithPrefix":"2600:381:6106:ce33::"},"pduSessionID":1,"pduType":"IPV4V6","ratType":"EUTRA","servingCNPlmnId":{"mcc":"310","mnc":"410"},"sscMode":"SSC_MODE_1","startTime":"2024-08-29T16:51:48Z","subscribedQoSInformation":{"5qi":8,"arp":{"preemptCap":"NOT_PREEMPT","preemptVuln":"PREEMPTABLE","priorityLevel":12},"priorityLevel":12},"subscribedSessionAMBR":{"downlink":"10 Gbps","uplink":"10 Gbps"}},"uetimeZone":"-04:00+1","userInformation":{"servedGPSI":"msisdn-12524127577","servedPEI":"imei-3551809589393307"},"userLocationinfo":{"eutraLocation":{"ecgi":{"eutraCellId":"be4e9c1","plmnId":{"mcc":"310","mnc":"410"}},"tai":{"plmnId":{"mcc":"310","mnc":"410"},"tac":"2693"}}}},"subscriberIdentifier":"imsi-310280109505161"}]
pattern1 = '\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d \[vert.x-eventloop-thread-\d+\] ERROR c.o.c.m.s.ChargingdataApiHandler - transactionId=(.*), subscriberId=imsi-(.*) - postChargingData - HTTP/2 - request that caused the error = \[accept=\*\/\*, content-type=application\/json, x-forwarded-proto=http, x-request-id=(.*), .*?"invocationTimeStamp":"(.*)","multipleUnitUsage".*?\{"nFFqdn":"(.*)","nFIPv4Address":".*?"dnnId":"(.*)","hPlmnId".*?"ratType":"(.*)","servingCNPlmnId".*?"startTime":"(.*)","subscribedQoSInformation".*?"eutraCellId":"(.*)","plmnId".*?,"subscriberIdentifier":"imsi-(.*)"\}\]'
#pattern2 = 2024-09-06 10:18:14,400 [vert.x-eventloop-thread-5] ERROR c.o.c.m.s.ChargingdataApiHandler - transactionId=cbbe6e36-986c-43d6-bea8-fc2b276a9b00, subscriberId=imsi-310280094022380 - postChargingData - HTTP/2 - status code = 400 - headers = [:status=400, content-type=application/problem+json, 3gpp-sbi-message-priority=24, content-length=92], body=[{"title":"Charging Service Error","status":400,"cause":"CHARGING_FAILED","invalidParams":[]}]
pattern2 = '\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d \[vert.x-eventloop-thread-\d+\] ERROR c.o.c.m.s.ChargingdataApiHandler - transactionId=(.*), subscriberId=imsi-(.*) - postChargingData - HTTP/2 - status code = 400 - headers = \[:status=400, content-type=application\/problem\+json, .*? body=\[{"title":"Charging Service Error","status":400,"cause":"CHARGING_FAILED","invalidParams":\[\]\}\]'
#pattern3 = 2024-09-06 11:16:16,589 [vert.x-eventloop-thread-5] ERROR c.o.c.m.s.ChargingdataApiHandler - transactionId=6434702b-fae8-4591-a9de-954fd87659ae, subscriberId=imsi-310280141991647 - postChargingData - ApiException during main flow
#com.openet.chf.stage.exception.FatalStageException: LocationDetection:: DATA Missing value: SgsnMCCMNC and/or SgsnAddress. Either one must be present
pattern3 = '\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d \[vert.x-eventloop-thread-\d+\] ERROR c.o.c.m.s.ChargingdataApiHandler - transactionId=(.*), subscriberId=imsi-(.*) - postChargingData - ApiException during main flow\ncom.openet.chf.stage.exception.FatalStageException: LocationDetection:: DATA Missing value: SgsnMCCMNC and\/or SgsnAddress. Either one must be present'

pattern1 = re.compile(pattern1)
pattern2 = re.compile(pattern2)
pattern3 = re.compile(pattern3, re.DOTALL)
def find_smf_loc_from_file(file_pattern):
    mapping_dict = {}
    mapping_400_list = []
    for file in glob.glob(file_pattern):
        print("Processing file: ", file)
        with open(file, 'r') as f:
            for line in f:
                data = re.search(pattern1, line)
                if data :
                    imsi = data.group(2)
                    trx_id = data.group(1)
                    invocationTimeStamp = data.group(4)
                    nFFqdn = data.group(5)
                    dnnId = data.group(6)
                    ratType = data.group(7)
                    startTime = data.group(8)
                    eutraCellId = data.group(9)
                    print(f'trx_id: {trx_id}, nFFqdn: {nFFqdn}, imsi: {imsi}, invocationTimeStamp: {invocationTimeStamp}, dnnId: {dnnId}, ratType: {ratType}, startTime: {startTime}, eutraCellId: {eutraCellId}')
                    if imsi not in mapping_dict:
                        mapping_dict[trx_id] = { "trx_id": trx_id, "imsi": imsi, "nFFqdn": nFFqdn, "invocationTimeStamp": invocationTimeStamp, "dnnId": dnnId, "ratType": ratType, "startTime": startTime, "eutraCellId": eutraCellId }
                data2 = re.search(pattern2, line)
                if data2:
                    trx_id = data2.group(1)
                    imsi = data2.group(2)
                    #print(f'trx_id: {trx_id}, imsi: {imsi}')
                    mapping_400_list.append(trx_id)
                data3 = re.search(pattern3, line)
                if data3:
                    trx_id = data3.group(1)
                    imsi = data3.group(2)
                    print(f'trx_id: {trx_id}, imsi: {imsi}')
                    mapping_400_list.append(trx_id)
    return( mapping_dict, mapping_400_list )

def find_smf_loc_from_pod():
    st, pod_list = subprocess.getstatusoutput("/usr/local/bin/kubectl get pods -n ecs | grep ^chf | awk '{print $1}'")
    if st != 0:
        print("Error in getting pods")
        return
    mapping_dict = {}
    mapping_400_list = []
    for pod in pod_list.split('\n'):
        print("Processing pod: ", pod)
        st, logs = subprocess.getstatusoutput(f"/usr/local/bin/kubectl logs {pod} -n ecs")
        if st != 0:
            print("Error in getting logs")
            return
        for line in logs.split('\n'):
            data = re.search(pattern1, line)
            if data :
                imsi = data.group(2)
                trx_id = data.group(1)
                invocationTimeStamp = data.group(4)
                nFFqdn = data.group(5)
                dnnId = data.group(6)
                ratType = data.group(7)
                startTime = data.group(8)
                eutraCellId = data.group(9)
                print(f'trx_id: {trx_id}, nFFqdn: {nFFqdn}, imsi: {imsi}, invocationTimeStamp: {invocationTimeStamp}, dnnId: {dnnId}, ratType: {ratType}, startTime: {startTime}, eutraCellId: {eutraCellId}')     
                if imsi not in mapping_dict:
                    mapping_dict[trx_id] = {"trx_id": trx_id, "imsi": imsi, "nFFqdn": nFFqdn, "invocationTimeStamp": invocationTimeStamp, "dnnId": dnnId, "ratType": ratType, "startTime": startTime, "eutraCellId": eutraCellId }
            data2 = re.search(pattern2, line)
            if data2:
                trx_id = data2.group(1)
                imsi = data2.group(2)
                #print(f'trx_id: {trx_id}, imsi: {imsi}')
                mapping_400_list.append(trx_id)
    return( mapping_dict, mapping_400_list )


def generate_csv_file( mapping_dict, mapping_400_list ):
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_file = f'failed_smf_fqdn_details_{now}.csv'
    writer = open(csv_file, 'w')
    csv_writer = csv.DictWriter(writer, fieldnames=["trx_id", "imsi", "nFFqdn", "invocationTimeStamp", "dnnId", "ratType", "startTime", "eutraCellId"])
    csv_writer.writeheader()
    for trx in set(mapping_400_list):
        if trx in mapping_dict:
            csv_writer.writerow(mapping_dict[trx])
    writer.close()
    print("CSV file generated: ", csv_file)

    #Based on CSV file, find number of IMSI for each SMF FQDN
    smf_imsi_count = {}
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for line in csv_reader:
            smf_fqdn = line[2]
            if smf_fqdn not in smf_imsi_count:
                smf_imsi_count[smf_fqdn] = 0
            smf_imsi_count[smf_fqdn] += 1
    #print("SMF FQDN and IMSI count: ", smf_imsi_count)
    smf_imsi_count = dict(sorted(smf_imsi_count.items(), key=lambda item: item[1], reverse=True))
    for key, value in smf_imsi_count.items():
        print(f'SMF FQDN: {key}, IMSI count: {value}')

if __name__ == "__main__":
    print('Select an option to find SMF location:')
    print('1. Find SMF location from log files')
    print('2. Find SMF location from POD logs')
    option = input('Enter option: ')
    if option == '1':
        file_pattern = input('Enter log file pattern: ')
        mapping_dict, mapping_400_list = find_smf_loc_from_file(file_pattern)
        generate_csv_file( mapping_dict, mapping_400_list )
    elif option == '2':
        mapping_dict, mapping_400_list = find_smf_loc_from_pod()
        generate_csv_file( mapping_dict, mapping_400_list )
    else:
        print("Invalid option")
        exit(1)
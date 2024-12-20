#!/usr/bin/python3

import os
import re
import json
from datetime import datetime
import subprocess

def find_schema(file_path):
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    os.makedirs(date, exist_ok=True)
    #name_pattern = '\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d .*? ERROR c.o.o.s.impl.stages.Aggregation -  - Skipping record due to exception. .*? error\[org.apache.kafka.streams.errors.StreamsException: Error encountered sending record to topic (.*) for task .*?'
    #name_pattern = '.*org.apache.kafka.streams.errors.StreamsException: Error encountered sending record to topic (.*) for .*?'

    #this will get event name
    name_pattern ='.*https://cl001.eastus2.prod.iebus.3pc.att.com:8082/subjects/(.*)\?.*'
    #name_pattern = '.*?org.apache.kafka.streams.errors.StreamsException: Exception caught in process. taskId=.*?, processor=.*?, topic=(.*), partition.*?'
    schema_name_pattern = re.compile(name_pattern)

    #This will get schema
    schema_patt = '.*DEBUG i.c.k.s.client.rest.RestService -  - Sending POST with input(.*) to https://cl001.eastus2.prod.iebus.3pc.att.com:8082/subjects/.*'
    schema_pattern = re.compile(schema_patt)

    schema_dict = {}
    counter = 1
    topic_name = None
    with open(file_path) as f:
        for line in f:
            schema = None
            re_schema_name = re.search(schema_name_pattern,line)
            if re_schema_name:
                topic_name = re_schema_name.group(1)
            re_schema = re.search(schema_pattern,line)
            if re_schema:
                schema = re_schema.group(1)
                print("----------\n",schema,"\n------------------")
                if schema[-1] == ']':
                    schema = schema[:-1]
                # Converting schema to json
                schema = json.loads(schema)
                schema=json.loads(schema['schema'])


            if topic_name and schema:
                if topic_name not in schema_dict:
                    schema_dict[topic_name] = set()
                if json.dumps(schema) not in schema_dict[topic_name]:
                    print(f'Writing schema in file for {topic_name}')
                    schema_dict[topic_name].add(json.dumps(schema, sort_keys=False, indent=2))
                    with open(f'{date}/{topic_name}_{counter}.json', 'w') as f:
                        #json.dump(schema, f, indent=4)
                        f.write(json.dumps(schema, sort_keys=False, indent=2))
                        f.write('\n')
                    counter += 1

def main():
    ns = 'cgf'
    option = input('Enter option (\n1: Choose option 1 for Pod(DEBUG LOGS)\n2: Choose option 2 for file(DEBUG LOGS)\n): ')
    if option == '1':
        pod_name = input('Enter pod name: ')
        file_path = f'{ns}_{pod_name}_schema_logs.log'
        st, pod_list = subprocess.getstatusoutput(f'/usr/local/bin/kubectl get pods -n {ns} -o jsonpath="{{.items[*].metadata.name}}"')
        for pod in pod_list.split():
            if pod.find(pod_name) != -1:
                subprocess.getstatusoutput(f'/usr/local/bin/kubectl logs {pod} -n {ns} >> {file_path}')
    elif option == '2':
        file_path = input('Enter the filename: ')
    else:
        print('Invalid option')
        return
    find_schema(file_path)

if __name__ == '__main__':
    main()

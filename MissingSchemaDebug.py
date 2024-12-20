#!/usr/bin/python3

import os
import re
import json
from datetime import datetime
import subprocess

def find_schema(file_path,log_level):
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    os.makedirs(date, exist_ok=True)

    if log_level == "ERROR":
        #this will get event name
        name_pattern = '.*org.apache.kafka.streams.errors.StreamsException: Error encountered sending record to topic (.*) for .*?'
        schema_patt = '.*org.apache.kafka.common.errors.SerializationException: Error retrieving Avro schema(.*)'
    elif log_level == "DEBUG":
        name_pattern = '.*https://cl001.eastus2.prod.iebus.3pc.att.com:8082/subjects/(.*)\?.*'
        schema_patt = '.*DEBUG i.c.k.s.client.rest.RestService -  - Sending POST with input(.*) to https://cl001.eastus2.prod.iebus.3pc.att.com:8082/subjects/.*'

    #name_pattern = '\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d .*? ERROR c.o.o.s.impl.stages.Aggregation -  - Skipping record due to exception. .*? error\[org.apache.kafka.streams.errors.StreamsException: Error encountered sending record to topic (.*) for task .*?' 

    schema_name_pattern = re.compile(name_pattern)
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
                if log_level== "DEBUG":
                    schema=json.loads(schema['schema'])


            if topic_name and schema:
                if topic_name not in schema_dict:
                    schema_dict[topic_name] = set()
                if json.dumps(schema) not in schema_dict[topic_name]:
                    print(f'Writing schema in file for {topic_name}')
                    schema_dict[topic_name].add(json.dumps(schema, sort_keys=False, indent=2))
                    with open(f'{date}/{topic_name}_{counter}.json', 'w') as f:
                        if log_level== "DEBUG":
                            f.write(json.dumps(schema, sort_keys=False, indent=2))
                        else:
                            json.dump(schema, f, indent=4)
                        f.write('\n')
                    counter += 1

def main():
    ns = 'cgf'
    option = input('Enter option (\n1: Choose option 1 for Pod & log level is ERROR,\n2: Choose option 2 for file & log level is ERROR,\n3: Choose option 3 for Pod & log level is DEBUG,\n4: Choose option 4 for file & log level is DEBUG): ')
    if option == '1':
        pod_name = input('Enter pod name: ')
        file_path = f'{ns}_{pod_name}_schema_logs.log'
        st, pod_list = subprocess.getstatusoutput(f'/usr/local/bin/kubectl get pods -n {ns} -o jsonpath="{{.items[*].metadata.name}}"')
        for pod in pod_list.split():
            if pod.find(pod_name) != -1:
                subprocess.getstatusoutput(f'/usr/local/bin/kubectl logs {pod} -n {ns} >> {file_path}')
                find_schema(file_path,"ERROR")
    elif option == '2':
        file_path = input('Enter the filename: ')
        find_schema(file_path,"ERROR")
    elif option == '3':
        pod_name = input('Enter pod name: ')
        file_path = f'{ns}_{pod_name}_schema_logs.log'
        st, pod_list = subprocess.getstatusoutput(f'/usr/local/bin/kubectl get pods -n {ns} -o jsonpath="{{.items[*].metadata.name}}"')
        for pod in pod_list.split():
            if pod.find(pod_name) != -1:
                subprocess.getstatusoutput(f'/usr/local/bin/kubectl logs {pod} -n {ns} >> {file_path}')
                find_schema(file_path,"DEBUG")
    elif option == '4':
        file_path = input('Enter the filename: ')
        find_schema(file_path,"ERROR")
    else:
        print('Invalid option')
        return
    

if __name__ == '__main__':
    main()

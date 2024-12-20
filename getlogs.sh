#!/bin/bash
for pod in `/usr/local/bin/kubectl get pods -n cgf | grep -i "six" | awk '{print $1}'`
do
echo "Getting logs for pod= $pod"
command= `/usr/local/bin/kubectl logs $pod -n cgf > ${pod}_3.log`
done
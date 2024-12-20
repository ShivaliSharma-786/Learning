#!/usr/bin/python3

import subprocess

def get_master_node():
    # Command to get the master node
    command = "/usr/local/bin/kubectl get nodes | grep -i m001 | awk -F ' ' '{print $1}'"
    master_node = subprocess.getoutput(command).strip()
    return master_node

def copy_kubeconfig_to_nodes(master_node, source_kubeconfig):
    # Get the list of all nodes
    nodes_command = "/usr/local/bin/kubectl get nodes -o name"
    nodes_output = subprocess.getoutput(nodes_command)
    nodes = nodes_output.splitlines()

    # Loop through each node and copy the kubeconfig file
    for node in nodes:
        node_name = node.replace("node/", "")
        if node_name != master_node:
            print(f"Copying kubeconfig to {node_name}...")
            copy_command = f"scp nccloud@{master_node}:{source_kubeconfig} {node_name}:nccloud@{source_kubeconfig}"
            subprocess.call(copy_command, shell=True)
            print(f"Kubeconfig copied to {node_name}")

    print("Kubeconfig copy completed.")

if __name__ == '__main__':
    # Define the source kubeconfig path
    source_kubeconfig = "/home/nccloud/.kube/config"

    # Get the master node
    master_node = get_master_node()
    print(f"Master node: {master_node}")

    # Copy kubeconfig to all nodes
    copy_kubeconfig_to_nodes(master_node, source_kubeconfig)
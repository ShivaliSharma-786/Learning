input_file = "/c:/Shivali Python Scripts/Learning/InputDNNs.txt"
routing_file = "/c:/Shivali Python Scripts/Learning/PrivateRoutingDNN.csv"

# Read the input DNNs from the file
with open(input_file, 'r') as f:
    input_dnns = f.read().splitlines()

# Read the routing DNNs from the file
with open(routing_file, 'r') as f:
    routing_dnns = f.read().splitlines()

# Loop through each input DNN
for dnn in input_dnns:
    if dnn in routing_dnns:
        print(f"DNN {dnn} is present")
    else:
        print(f"DNN {dnn} is absent")
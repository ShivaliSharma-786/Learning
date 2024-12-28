d={1:"Shivali",2:"Neeta",3:"shubham"}
print(d)
print(d.items())
print(d.keys())

for key in d.keys():
    print(d[key])

print(d.values())

#Delete a value
del d[3]
print(d)
ls=["Shivali","Sharma","Sharma",6,"SRE"]
print(ls[-1])
print(ls[3])
print(ls[2:4])
print(ls*2)
print(len(ls))

#append
ls.append([9,-99.02])
print(ls)

#Extend
ls.extend([9,-99.02])
print(ls)

#Remove
ls.remove("Sharma")
print(ls)

#Delete
del(ls[-1])
print(ls)

#Clear/Empty a list
ls.clear()
print(ls)

#Max & Min functions
ls=[5,900.44,-45.65,0.228,123]
print(max(ls))
print(min(ls))

#insert at an index
ls.insert(1,99)
print(ls)

#Sort the list
ls.sort() # increasing order
print(ls)
ls.sort(reverse=True)
print(ls)
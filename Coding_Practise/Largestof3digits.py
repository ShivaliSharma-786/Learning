def findlargestofthree(ls):
    largest=ls[0]
    if ls[1]>largest:
        largest=ls[1]
    if ls[2]>largest:
        largest=ls[2]
    return largest

ls=[int(val) for val in input("Enter 3 nos ").split()]
res=findlargestofthree(ls)
print(res)
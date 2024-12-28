def oddnos(start,end):
    if start%2 ==0:
        start+=1
    for i in range(start,end+1,2):
        print(i)

start,end=[int(val) for val in input("enter 2 nos").split()]
oddnos(start,end)
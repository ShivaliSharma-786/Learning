def printTable(val,start=1,end=10):
    for i in range(start,end+1):
        print(val,"*",i,"=",val*i)

printTable(5,10,20)
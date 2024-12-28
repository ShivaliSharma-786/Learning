# Series are: 0,1,1,2,3,5


def series(no):
    if no ==1:
        return([0])
    elif no==2:
        return([0,1])
    else:
        a=0
        b=1
        res=[0,1]
        for i in range(3,no+1):
            c=a+b
            res.append(c)
            a=b
            b=c
        return(res)
    
res=series(3)
print(res)

# and , or & not

def logicalOperators():
    a,b=[ int(val) for val in input("Enter 2 nos").split()]

    print(a>b and b<a)
    print(a>b or b<a)
    print(not(a>b))
    
logicalOperators()
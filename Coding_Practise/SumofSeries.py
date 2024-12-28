import math

def fact(no):
    if no == 0 or no==1:
        return 1
    else:
        res=no*fact(no-1)
        return res
    
'''
def series(n):
    add=0
    for i in range(1,n+1):
        add += 1/fact(i)
    print(add)
'''
import math
def series(no):
    add=0
    for i in range(1,no+1):
        add += 1/math.factorial(i)
    print(add)

series(2)


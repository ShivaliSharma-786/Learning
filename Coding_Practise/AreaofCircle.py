# formaula: sqrt(s(s-a)*(s-b)*(s-c))
import math
def areaofCircle():
    a,b,c=[int(val) for val in input("Enter 3 nos").split()]
    s=(a+b+c)/2
    val=math.fabs(s*(s-a)*(s-b)*(s-c))
    print(val)
    print(math.sqrt(val))

areaofCircle()
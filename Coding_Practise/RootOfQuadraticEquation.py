#formula: -b + math.sqrt(b**2 - 4*a*c)/2*a & -b - math.sqrt(b**2 - 4*a*c)/2*a
import math
def squareRoots():
    a,b,c=[int(val) for val in input("Enter 3 nos").split()]
    x=math.fabs(b**2 - 4*a*c)
    print("First Root is", (-b + math.sqrt(x))/(2*a) )
    print("Second Root is", (-b - math.sqrt(x))/(2*a) )

squareRoots()
import math
def getResult(ls):
    for marks in ls:
        if marks<35:
            print("fail")
            exit(0)
    avg=math.fsum(ls)/3
    if avg<=59:
        print("C Grade")
    elif avg<=69:
        print("B Grade")
    else:
        print("A Grade")

ls=[int(val) for val in input("Enter marks in 3 subjects").split()]
getResult(ls)
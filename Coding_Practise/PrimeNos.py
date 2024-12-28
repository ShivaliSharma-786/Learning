#When a no is divisibe by 1 or the no itself then a no is prime.

def findPrime(no):
    if no == 2 or no ==1:
        return "Prime"
    else:
        res="Prime"
        for i in range(2,(no//2)+1):
            if no % i== 0:
                res= "NOT Prime"
        return res

res=findPrime(40)
print(res)
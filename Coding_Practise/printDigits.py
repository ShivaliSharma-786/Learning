def getDigits(no):
    ls=[]
    while no>0:
        digit=no%10
        print(digit)
        ls.append(digit)
        no=no//10
    print(ls[-1::-1])

getDigits(1897)
def ReverseAndSumOFDigits(no):
    org=no
    rev=0
    sum=0
    prod=1
    while no>0:
        digit=no%10
        sum+=digit
        prod*=digit
        rev=rev*10+digit
        no=no//10
    print("reverse is= ",rev)
    print("sum of digits is= ",sum)
    print("product of digits is=",prod)
    if rev == org:
        print("Plaindrome")
    else:
        print("Not Plaindrome")

ReverseAndSumOFDigits(121)
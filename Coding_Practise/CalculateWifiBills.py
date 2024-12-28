'''
Mandatory Monthy rent = 160
1. First 28GB is Free
2. 28GB- 60GB is Rs10/GB
3. 60GB-100GB is Rs25/GB
4. Above 100GB is Rs50/GB
'''

def CalculateBill(amt):
    if amt<=28:
        charge=160
    elif amt<=60:
        charge=160+(amt-28)*10
    elif amt <=100:
        charge= 160+ 32*10 + (amt-60)*25
    else:
        charge=160 + 32*10 + 40*25 + (amt-100)*50
    return charge

res=CalculateBill(int(input("Enter a no")))
print(res)
'''
def findEven(no):
    if no%2 ==0:
        print("Even")
    else:
        print("Odd")


no=int(input("Enter a no"))
findEven(no)

'''
'''
def findEven(start,end):
    if start%2 !=0:
        start +=1
    for val in range(start,end+1,2):
        print(val)

start,end=[int(val) for val in input("Enter 2 nos").split()]
findEven(start,end)
'''

def findEven(x):
    if x%2==0: print("Even")
    else: print("Odd")

findEven(7)
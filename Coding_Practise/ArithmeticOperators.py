# Arithemetics Opertors

def calculator(no1,no2,choice):
    if choice not in range(0,8):
        print("Invalid Choice")
    else:
        if choice == 1:
            print(no1+no2)
        elif choice ==2:
            print(no1-no2)
        elif choice == 3:
            print(no1*no2)
        elif choice == 4:
            print(no1/no2)
        elif choice ==5 :
            print(no1//no2)
        elif choice == 6:
            print(no1%no2)
        else:
            print(no1**no2)


choice=True
while(choice):
    no1,no2=[int(val) for val in input("Enter 2 nos: ").split()]
    print("Enter 1 for sum: +")
    print("Enter 2 for sub: =")
    print("Enter 3 for prod: *")
    print("Enter 4 for division: / Quotient with decimal")
    print("Enter 5 for floor division: // Quotient without decimal ")
    print("Enter 6 for remainder: % modulas")
    print("Enter 7 for power: **")
    print("Enter 8 to quit")
    choice=int(input("Enter your choice"))
    if choice == 8:
        break
    else:
        calculator(no1,no2,choice)

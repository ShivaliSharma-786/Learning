# Find no of years, months, weeks & days

def findYearMonthsWeeksDays(no):
    years=no//365
    months=(no%365)//30
    weeks=((no%365)%30) // 7
    days =((no%365)%30) % 7
    print("yaers are :",years)
    print("Months are :",months)
    print("Weeks are ",weeks)
    print("Days are :",days)

findYearMonthsWeeksDays(500)

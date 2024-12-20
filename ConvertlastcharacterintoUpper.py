def convertUpper(s):
    s=s.strip()
    s=s+" "
    res=""
    print(s)
    for i in range(0,len(s)):
        if s[i]!=" " and s[i+1]==" ":
            res+=s[i].upper()
        else:
            res+=s[i]
    print(res)
            








#------------------------------Funcation Call---------------------
convertUpper("Lets convert last character into upper case")
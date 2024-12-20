def hashAlernate(s):
    res=""
    for i in range(0,len(s)):
        if s[i].isupper()== True:
            if(s[i+1].isupper()== False):
                res+=("#"+ s[i])
            else: 
                res+=s[i]
        elif(s[i]==" "):
            res+=s[i]
        elif (s[i].isupper()== False):
            res+=(s[i] + "#")
    print(res)


#------------------------------
hashAlernate("shiVali ShaRma")
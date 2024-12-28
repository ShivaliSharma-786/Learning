s="""
Hello, How are you doing??
My name is Laila.
I live in Arvin, which is Duke's Heardth's estate. 
"""
print(s)
print(s[3])
print(s[2:6])
print(s*3)

str = "GeeksforGeeks" 
# startswith()
print(str.startswith("Geeks"))
print(str.startswith("Geeks", 4, 10))
print(str.startswith("Geeks", 8, 14))
 
print("\n")
 
# endswith
print(str.endswith("Geeks"))
print(str.endswith("Geeks", 2, 8))
print(str.endswith("for", 5, 8))

#Slicing
a="Shivali"
print(a.startswith("S"))
print(a[2:])
print(a[0:])
print(a[:4])
print(a[-4:])
print(a[0::2])
# reverse a string
print(a[len(a)::-1])

#Strip
x="   Shivali sharma   "
print(x.strip())
print(x.lstrip())
print(x.rstrip())

#find
print(a.find("ali"))
print(a.find("iva",2,5))

#count
print(a.count("ali"))

#Replace
print(a.replace("ali","Shakti"))

#upper/lower/title
print(a.upper())
print(a.lower())
print(x.title())
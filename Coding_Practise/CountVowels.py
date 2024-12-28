def CountVowels(st):
    st=st.lower()
    count=0
    for i in st:
        if i in ['a','e','i','o','u']:
            count+=1
    return count

print(CountVowels(input("Enter a string")))

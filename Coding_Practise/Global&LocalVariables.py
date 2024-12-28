x=123
def display():
    print(globals()['x'])
    x=34
    print(x)
    globals()['x']+=2
    print(globals()['x'])

display()

def Display(name):
    def sayHello():
        return "Hello!,"
    return sayHello() + name +":)"
f=Display
print(f("Shivali"))
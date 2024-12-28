def display():
    def prints():
        return "Hello! How you doing?"
    return prints()
print(display())

def displayName(name):
    def sayHello():
        return "Hello!"
    return sayHello() + name + ":)"

print(displayName("Shivali"))
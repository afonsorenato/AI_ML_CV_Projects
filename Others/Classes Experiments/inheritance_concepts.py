class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print(f"I am {self.name} and I am {self.age} years old")



# Inheritance
class Cat(Pet):
    def speak(self):
        print("Meow")


class Dog(Pet):
    def speak(self):
        print("Bark")


p = Pet("Tim", 19)
p.show()
c = Cat("Bill", 34)
c.show()
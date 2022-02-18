class Dog:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def add_one(self, x):
        return x+1

    def get_name(self):
        return self.name

    def set_age(self, age):
        self.age = age

    def bark(self):
        print("bark")

    def get_age(self):
        return self.age


d = Dog("Tim", 34)
print(d.name)
d2 = Dog("Bill", 12)
print(d2.name)

#1
class Person:
    def __init__(self):
        print("Person created")

p = Person()


#2
class Dog:
    def __init__(self, name):
        self.name = name
        print("Dog name is", self.name)

d = Dog("Buddy")


#3
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

s = Student("Anna", 16)
print(s.name, s.age)


#4
class Car:
    def __init__(self, brand):
        self.brand = brand

    def show(self):
        print("Car brand:", self.brand)

c = Car("Toyota")
c.show()


#5
class Book:
    def __init__(self, title):
        self.title = title
        print("Book title:", self.title)

b = Book("Python Basics")

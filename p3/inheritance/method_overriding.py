#1
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def speak(self):
        print("Dog barks")

a = Animal()
d = Dog()
a.speak()
d.speak()


#2
class Person:
    def introduce(self):
        print("Hello, I am a person.")

class Student(Person):
    def introduce(self):
        super().introduce()
        print("I am also a student.")

s = Student()
s.introduce()


#3
class Shape:
    def area(self):
        print("Area not defined")

class Rectangle(Shape):
    def area(self):
        length = 4
        width = 6
        print("Area:", length * width)

r = Rectangle()
r.area()

#4
class Bird:
    def fly(self):
        print("Bird can fly")

class Penguin(Bird):
    def fly(self):
        print("Penguin cannot fly")

birds = [Bird(), Penguin()]
for b in birds:
    b.fly()
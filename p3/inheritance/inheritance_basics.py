#1
class Animal:
    def speak(self):
        return "I make a sound."
class Dog(Animal):
    def speak(self):
        return "I bark."
dog = Dog()
print("1.", dog.speak())

#2
class Vehicle:
    def info(self):
        return "I am a vehicle."
class Car(Vehicle):
    def info(self):
        return "I am a car."
car = Car()
print("2.", car.info())

#3
class Person:
    def greet(self):
        return "Hello!"
class Student(Person):
    def greet(self):
        return "Hi, I am a student!"
s = Student()
print("3.", s.greet())

#4
class Shape:
    def area(self):
        return 0
class Square(Shape):
    def area(self):
        return 5 * 5
sq = Square()
print("4. Area of square:", sq.area())

#5
class Bird:
    def fly(self):
        return "I can fly!"
class Parrot(Bird):
    def fly(self):
        return "I fly high!"
p = Parrot()
print("5.", p.fly())

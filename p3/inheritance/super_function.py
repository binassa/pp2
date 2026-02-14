#1
class Person:
    def __init__(self, name):
        self.name = name
class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade
s = Student("Anna", "12th")
print("1.", s.name, s.grade)

#2
class Vehicle:
    def __init__(self, brand):
        self.brand = brand
    def info(self):
        return f"Vehicle: {self.brand}"
class Car(Vehicle):
    def __init__(self, brand, model):
        super().__init__(brand)
        self.model = model
    def info(self):
        return f"{super().info()}, Model: {self.model}"
car = Car("Toyota", "Corolla")
print("2.", car.info())

#3
class Animal:
    def speak(self):
        return "Some sound"
class Dog(Animal):
    def speak(self):
        return super().speak() + " and Bark!"
d = Dog()
print("3.", d.speak())

#4

class A:
    def greeting(self):
        return "Hello from A"
class B(A):
    def greeting(self):
        return super().greeting() + " and B"
b = B()
print("5.", b.greeting())

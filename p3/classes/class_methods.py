#1
class Person:
    count = 0

    def __init__(self):
        Person.count += 1

    @classmethod
    def show_count(cls):
        print("Total persons:", cls.count)

p1 = Person()
p2 = Person()
Person.show_count()


#2
class Student:
    school = "ABC School"

    @classmethod
    def show_school(cls):
        print("School name:", cls.school)

Student.show_school()


#3
class Car:
    wheels = 4

    @classmethod
    def info(cls):
        print("Cars have", cls.wheels, "wheels")

Car.info()


#4
class Book:
    category = "Education"

    @classmethod
    def change_category(cls, new_category):
        cls.category = new_category

    @classmethod
    def show_category(cls):
        print("Category:", cls.category)

Book.show_category()
Book.change_category("Programming")
Book.show_category()


#5
class Animal:
    type = "Mammal"

    @classmethod
    def show_type(cls):
        print("Animal type:", cls.type)

Animal.show_type()

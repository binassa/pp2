#1
class Father:
    def skill1(self):
        print("Father: Gardening")

class Mother:
    def skill2(self):
        print("Mother: Cooking")

class Child(Father, Mother):
    pass

c = Child()
c.skill1()
c.skill2()


#2
class A:
    def show(self):
        print("Class A")

class B:
    def display(self):
        print("Class B")

class C(A, B):
    pass

obj = C()
obj.show()
obj.display()


#3
class Writer:
    def write(self):
        print("Writing a book")

class Speaker:
    def speak(self):
        print("Giving a speech")

class Author(Writer, Speaker):
    pass

a = Author()
a.write()
a.speak()


#4
class Math:
    def add(self, a, b):
        print("Sum:", a + b)

class Multiply:
    def multiply(self, a, b):
        print("Product:", a * b)

class Calculator(Math, Multiply):
    pass

calc = Calculator()
calc.add(5, 3)
calc.multiply(5, 3)


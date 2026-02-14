#1
def greet(name):
    return "Hello, " + name + "!"
#2
def add(a, b):
    return a + b
#3
def is_even(n):
    return n % 2 == 0
#4
def max_of_three(a, b, c):
    return max(a, b, c)
#5
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
#1 create
def my_function():
  print("Hello from a function")

#2 call
def my_function():
  print("Hello from a function")
my_function()

#3
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

#4
def get_greeting():
  return "Hello from a function"

print(get_greeting())

#5
def my_function():
  pass
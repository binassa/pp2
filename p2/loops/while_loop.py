#1
i = 1
while i <= 5:
    i = i + 1
    print(i)
#2
password = ""
while password != "1234":
    password = input("enter password: ")
print("access")
#3
total = 0
n = int(input())

while n != 0:
    total = total + n
    n = int(input())
print(total)
#4
while True:
    word = input()
    if word == "stop":
        break
    print(word)

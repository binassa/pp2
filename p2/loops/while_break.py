#1
while True:
    n = int(input())
    if n == 0:
        break
    print(n)
#2
while True:
    word = input()
    if word.lower() == "stop":
        break
    print(word)
#3
i = int(input())
while True:
    print(i)
    i += 1
    if i > 10:
        break
#4
words = ["apple", "banana", "cherry", "date"]
i = 0
while i < len(words):
    print(words[i])
    if words[i] == "cherry":
        break
    i += 1
#5
while True:
    n = int(input())
    if n < 0:
        print()
        break
    print(n)

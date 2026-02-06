#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
  
#2
nums = input().split()

for n in nums:
    if n == "5":
        break
    print(n)

#3
for i in range(1, 4):
    for j in range(1, 4):
        if j == 2:
            break
        print(i, j)

#4
while True:
    word = input("Enter a word: ")
    if word == "":
        break
    print(word)
#5
word = "python"

for ch in word:
    if ch == "h":
        break
    print(ch)

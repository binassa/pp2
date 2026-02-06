#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)
#2
for i in range(1, 6):
    if i % 2 == 0:
        continue
    print(i)
#3
nums = [3, -2, 7, -5, 8]

for n in nums:
    if n < 0:
        continue
    print(n)
#4
num = input().split()
for n in num:
   if int(n) > 0:
      continue
   print(n)
#5
num = input().split()
for n in num:
    if int(n) % 3 == 0:
        continue
    print(n)

#1
i = -3
while i < 5:
    i += 1
    if i < 0:
        continue
    print(i)

#2
i = int(input())
while i < 10000:
    i += 10
    if i % 4 != 0:
        continue
    print(i)

#3
i = 0
while i < 10:
    i += 1
    if i % 3 == 0:
        continue
    print(i)

#4
i = int(input())
while i < 100:
    i += 5
    if i % 20 != 0:
        continue
    print(i)
#5
i = int(input())
while i < 99:
    i += 11
    if i % 22 != 0:
        continue
    print(i)
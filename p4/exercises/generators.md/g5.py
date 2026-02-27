def countdown(n):
    for i in range(n, -1, -1):
        yield i

n = int(input("number: "))

print(n)
for number in countdown(n):
    print(number)
#1
fruits = ["apple", "banana", "cherry", "date"]

print("Enumerate example:")
for index, fruit in enumerate(fruits, start=1):  # start=1 чтобы индексация начиналась с 1
    print(index, fruit)
#2
fruits = ["apple", "banana", "cherry"]
prices = [100, 200, 150]

print("Zip example:")
for fruit, price in zip(fruits, prices):
    print(f"{fruit} costs {price} KZT")

#3
n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

dot = sum(x * y for x, y in zip(a, b))
print(dot)

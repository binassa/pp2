def square(a, b):
    for i in range(a, b + 1):
        yield i ** 2

start = int(input("a: "))
end = int(input("b: "))

print("sq from", start, "to", end, ":")
for sq in square(start, end):
    print(sq)
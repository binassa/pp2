def divisible_by_3_4(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
print(",".join(str(num) for num in divisible_by_3_4(n)))
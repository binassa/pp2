nums = [1, 2, 3, 4, 5, 6]
#1
doubled = list(map(lambda x: x * 2, nums))
print("Map result:", doubled)

#2
evens = list(filter(lambda x: x % 2 == 0, nums))
print("Filter result:", evens)


#3
from functools import reduce
nums = [1, 2, 3, 4, 5]

total = reduce(lambda x, y: x + y, nums)
print("Reduce result:", total)

#4
from functools import reduce
nums = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, nums)
print(product) 
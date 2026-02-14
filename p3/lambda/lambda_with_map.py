#1
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)
#2
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
print("1. Squares:", squares)
#3
words = ["hello", "world", "python"]
upper_words = list(map(lambda w: w.upper(), words))
print("2. Uppercase:", upper_words)
#4
nums = [10, 20, 30, 40]
added = list(map(lambda x: x + 5, nums))
print("3. Add 5:", added)
#5
list1 = [1, 2, 3]
list2 = [4, 5, 6]
sum_lists = list(map(lambda x, y: x + y, list1, list2))
print("4. Sum of two lists:", sum_lists)
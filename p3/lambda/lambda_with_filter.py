#1
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("1. Even numbers:", evens)
#2
odds = list(filter(lambda x: x % 2 != 0, numbers))
print("2. Odd numbers:", odds)
#3
words = ["hi", "hello", "cat", "python"]
long_words = list(filter(lambda w: len(w) > 3, words))
print("3. Words with length > 3:", long_words)
#4
nums = [-5, 3, -2, 8, 0, 7]
positives = list(filter(lambda x: x > 0, nums))
print("4. Positive numbers:", positives)
#5
nums2 = [1, 3, 6, 10, 12, 15]
div3 = list(filter(lambda x: x % 3 == 0, nums2))
print("5. Divisible by 3:", div3)
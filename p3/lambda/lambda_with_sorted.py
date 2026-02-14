#1
numbers = [5, 2, 9, 1, 7]
sorted_numbers = sorted(numbers)
print("1. Ascending:", sorted_numbers)
#2
desc_numbers = sorted(numbers, reverse=True)
print("2. Descending:", desc_numbers)
#3
words = ["apple", "hi", "banana", "cat"]
sorted_by_length = sorted(words, key=lambda w: len(w))
print("3. By length:", sorted_by_length)
#4
sorted_by_last_letter = sorted(words, key=lambda w: w[-1])
print("4. By last letter:", sorted_by_last_letter)
#5
pairs = [(1, 5), (2, 3), (3, 4)]
sorted_by_second = sorted(pairs, key=lambda x: x[1])
print("5. By second element:", sorted_by_second)
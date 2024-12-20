L = [5, 11, 19, 4, 21, 67, 10]

# Separate odd and even numbers
odd_nums = [num for num in L if num % 2 != 0]
even_nums = [num for num in L if num % 2 == 0]

# Sort even numbers in ascending order
even_nums.sort()

# Sort odd numbers in descending order
odd_nums.sort(reverse=True)

# Combine the sorted lists
sorted_nums = even_nums + odd_nums

print(sorted_nums)


def max_possible_number(N):
    def sum_of_digits(num):
        return sum(int(digit) for digit in str(num))

    x = 0
    while N - sum_of_digits(x) != x:
        x += 1

    return x

# Example usage
N = 12345
Z = max_possible_number(N)
print(Z)
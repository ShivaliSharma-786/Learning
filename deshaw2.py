def findWinner(s, k):
    # Function to count total removals
    def count_removals(s):
        removals = 0
        stack = []
        for char in s:
            if stack and stack[-1] == char:
                stack.pop()
                removals += 1
            else:
                stack.append(char)
        return removals

    total_removals = count_removals(s)
    # Determine the loser based on the total number of removals
    loser = (total_removals % k) + 1
    return loser

# Example usage
s = "baabzzpq"
k = 4
loser = findWinner(s, k)
print(f"The player who loses is: Player {loser}")
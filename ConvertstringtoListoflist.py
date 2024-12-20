input_string = "ABC PQRS WXYZ"
output = []

# Split the input string by spaces
words = input_string.split()

# Iterate over each word
for word in words:
    # Convert each word into a list of characters
    char_list = list(word)
    output.append(char_list)

print(output)
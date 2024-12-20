"""
Write a program which takes input string as "ABC PQRS WXYZ" and return the output string as "APW BQX CRY DSZ"

"""

def rearrange_string(input_string):
    words = input_string.split()
    output_string = ""

    for i, word in enumerate(words):
        for j, char in enumerate(word):
            if j % 2 == 0:
                output_string += char
            else:
                output_string += words[i-1][j]

        if i < len(words) - 1:
            output_string += " "

    return output_string

input_string = "ABC PQRS WXYZ"
output_string = rearrange_string(input_string)
print(output_string)
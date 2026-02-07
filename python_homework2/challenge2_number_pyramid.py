"""
Challenge 2: Number Pyramid Pattern
===================================
Task: Print a pyramid pattern of numbers using nested loops.

Expected output:
1
12
123
1234
12345
123456
1234567
12345678
"""


def print_number_pyramid(rows):
    """
    Print a number pyramid pattern.

    Args:
        rows: Number of rows in the pyramid
    """
    # Outer loop controls the number of rows
    # range(1, rows+1) gives us 1, 2, 3, ..., rows
    for i in range(1, rows + 1):
        # Inner loop prints numbers from 1 to current row number
        # range(1, i+1) gives us 1, 2, 3, ..., i
        for j in range(1, i + 1):
            # end='' prevents print from adding newline after each number
            print(j, end='')
        # Print newline after each row is complete
        print()


# Print the pyramid with 8 rows
print("Number pyramid pattern (8 rows):")
print_number_pyramid(8)

# Alternative: Using string multiplication
print("\nAlternative method using string join:")
for i in range(1, 9):
    # ''.join() concatenates list items into a string
    # str(j) converts each number to a string
    print(''.join(str(j) for j in range(1, i + 1)))
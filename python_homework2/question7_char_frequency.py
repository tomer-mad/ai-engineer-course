"""
Question 7: Count Character Frequency in String
===============================================
Task: Build a function that counts how many times each character
appears in a string and returns a dictionary.

Example:
Input: 'HANNA'
Output: {'H': 1, 'A': 2, 'N': 2}
"""


def count_characters(input_string):
    """
    Count the frequency of each character in a string.

    Args:
        input_string: The string to analyze

    Returns:
        Dictionary with characters as keys and their counts as values
    """
    # Create an empty dictionary to store character counts
    char_count = {}

    # Iterate through each character in the string
    for char in input_string:
        # Check if character already exists in our dictionary
        if char in char_count:
            # If yes, increment its count
            char_count[char] += 1
        else:
            # If no, add it with count of 1
            char_count[char] = 1

    return char_count


# Alternative implementation using get() method
def count_characters_alt(input_string):
    """Alternative implementation using get() method."""
    char_count = {}
    for char in input_string:
        # get() returns the value for key if exists, otherwise returns default (0)
        char_count[char] = char_count.get(char, 0) + 1
    return char_count


# Test with the example
test_string = "HANNA"
print("Character frequency counter:")
print(f"Input string: '{test_string}'")
print(f"Character counts: {count_characters(test_string)}")
print(f"Alt method result: {count_characters_alt(test_string)}")

# Additional test
print(f"\nInput string: 'MISSISSIPPI'")
print(f"Character counts: {count_characters('MISSISSIPPI')}")
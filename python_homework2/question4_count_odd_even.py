"""
Question 4: Count Odd and Even Numbers with String Detection
============================================================
Task: Count odd and even numbers in a list. If a string is encountered,
use break and reset counters to zero.
"""


def count_odd_even(numbers_list):
    """
    Count odd and even numbers in a list.
    If a string is found, print message and reset counters.

    Args:
        numbers_list: List containing integers (and possibly strings)
    """
    # Initialize counters for odd and even numbers
    odd_count = 0
    even_count = 0

    # Iterate through each element in the list
    for num in numbers_list:
        # Check if the element is a string using isinstance()
        # isinstance() checks if an object is of a specific type
        if isinstance(num, str):
            print("It's a string!")
            # Reset both counters to zero as per requirements
            odd_count = 0
            even_count = 0
            # break exits the loop immediately
            break

        # Check if number is even or odd using modulo operator (%)
        # If a number divided by 2 has remainder 0, it's even
        if num % 2 == 0:
            even_count += 1  # Increment even counter
        else:
            odd_count += 1   # Increment odd counter

    # Print the final counts
    print(f"Number of even numbers: {even_count}")
    print(f"Number of odd numbers: {odd_count}")


# Test with a list of only numbers
print("Test 1 - Numbers only:")
count_odd_even([1, 2, 3, 4, 5, 6, 7, 8, 9])

# Test with a list containing a string
print("\nTest 2 - With string:")
count_odd_even([1, 2, 3, 4, "Oops", 6, 7, 8, 9])
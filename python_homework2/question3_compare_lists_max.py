"""
Question 3: Compare Two Lists and Find Maximum Values
=====================================================
Task: Create a program that takes two lists of same length and returns
a new list with the maximum value at each index position.
"""


def compare_lists_max(lst1, lst2):
    """
    Compare two lists and return a new list with maximum values at each index.

    Args:
        lst1: First list of integers
        lst2: Second list of integers

    Returns:
        A new list with the larger value at each position

    Raises:
        ValueError: If lists are not the same length
    """
    # First, check if both lists have the same length
    # len() returns the number of elements in a list
    if len(lst1) != len(lst2):
        raise ValueError("Error: Lists must be of the same length!")

    # Create an empty list to store our results
    result = []

    # Iterate through both lists simultaneously using range and len
    # range(len(lst1)) generates indices from 0 to length-1
    for i in range(len(lst1)):
        # max() returns the larger of two values
        # We compare elements at the same index from both lists
        result.append(max(lst1[i], lst2[i]))

    return result


# Test with the example from the homework
list1 = [1, 2, 3, 4, 5]
list2 = [5, 4, 3, 2, 1]

print("Maximum values from two lists:")
print(f"List 1: {list1}")
print(f"List 2: {list2}")

result_list = compare_lists_max(list1, list2)
print(f"Maximum values: {result_list}")

# Test error handling with different length lists
print("\nTesting error handling:")
try:
    compare_lists_max([1, 2, 3], [1, 2])
except ValueError as e:
    print(f"Error caught: {e}")
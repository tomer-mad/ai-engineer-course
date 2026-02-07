"""
Challenge 1: Get Unique Elements from List
==========================================
Task: Create a function that returns only unique elements from a list.

Example:
Input: [1, 2, 3, 3, 3, 3, 4, 5]
Output: [1, 2, 3, 4, 5]
"""


def get_unique_elements(input_list):
    """
    Return a new list containing only unique elements from the input list.
    Preserves the original order of first occurrence.

    Args:
        input_list: List that may contain duplicates

    Returns:
        New list with only unique elements
    """
    # Method: Using a loop to preserve order
    unique_list = []
    for item in input_list:
        # Only add if item not already in unique_list
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


# Alternative using dict.fromkeys() - preserves order in Python 3.7+
def get_unique_elements_alt(input_list):
    """Alternative implementation using dict.fromkeys()."""
    # dict.fromkeys() creates a dict with keys from the list
    # Since dict keys are unique, duplicates are removed
    # list() converts the keys back to a list
    return list(dict.fromkeys(input_list))


# Test with the example
test_list = [1, 2, 3, 3, 3, 3, 4, 5]
print("Get unique elements from list:")
print(f"Input: {test_list}")
print(f"Unique elements: {get_unique_elements(test_list)}")
print(f"Using dict.fromkeys(): {get_unique_elements_alt(test_list)}")

# Additional test with strings
test_list2 = ['a', 'b', 'a', 'c', 'b', 'd']
print(f"\nInput: {test_list2}")
print(f"Unique elements: {get_unique_elements(test_list2)}")
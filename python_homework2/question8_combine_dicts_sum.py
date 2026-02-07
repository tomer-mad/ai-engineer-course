"""
Question 8: Combine Dictionaries by Adding Values for Common Keys
=================================================================
Task: Merge two dictionaries, adding values together if keys match.

Sample input:
d1 = {'a': 100, 'b': 200, 'c': 300}
d2 = {'a': 300, 'b': 200, 'd': 400}

Expected output: {'a': 400, 'b': 400, 'd': 400, 'c': 300}
"""


def combine_dicts_sum_values(d1, d2):
    """
    Combine two dictionaries, summing values for keys that exist in both.

    Args:
        d1: First dictionary
        d2: Second dictionary

    Returns:
        New dictionary with combined values
    """
    # Start with a copy of the first dictionary
    # Using .copy() to avoid modifying the original
    result = d1.copy()

    # Iterate through the second dictionary
    for key, value in d2.items():
        # items() returns key-value pairs as tuples
        if key in result:
            # If key exists in both, add the values together
            result[key] += value
        else:
            # If key only in d2, add it to result
            result[key] = value

    return result


# Define the sample dictionaries
d1 = {'a': 100, 'b': 200, 'c': 300}
d2 = {'a': 300, 'b': 200, 'd': 400}

print("Combine dictionaries with value addition:")
print(f"d1 = {d1}")
print(f"d2 = {d2}")

combined = combine_dicts_sum_values(d1, d2)
print(f"\nCombined: {combined}")
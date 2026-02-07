"""
Question 5: Generate Dictionary with (x, x+3) Pattern
=====================================================
Task: Create a dictionary where keys are numbers 1 to n,
and values are key + 3.

Sample output for n=5: {1: 4, 2: 5, 3: 6, 4: 7, 5: 8}
"""


def generate_x_plus_3_dict(n):
    """
    Generate a dictionary with numbers 1 to n as keys and key+3 as values.

    Args:
        n: The upper limit (inclusive)

    Returns:
        Dictionary in form {1: 4, 2: 5, ..., n: n+3}
    """
    # Dictionary comprehension - a concise way to create dictionaries
    # Syntax: {key: value for variable in iterable}
    # range(1, n+1) generates numbers from 1 to n (inclusive)
    return {x: x + 3 for x in range(1, n + 1)}


# Test with n = 5
n = 5
result_dict = generate_x_plus_3_dict(n)
print(f"Dictionary with (x, x+3) pattern:")
print(f"n = {n}")
print(f"Result: {result_dict}")

# Additional test with different n
print(f"\nn = 10")
print(f"Result: {generate_x_plus_3_dict(10)}")
"""
Question 6: Concatenate Multiple Dictionaries
=============================================
Task: Merge three dictionaries into one new dictionary.

Sample input:
dic1 = {1:10, 2:20}
dic2 = {3:30, 4:40}
dic3 = {5:50, 6:60}

Expected output: {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}
"""


def concatenate_dicts(*dicts):
    """
    Concatenate multiple dictionaries into one.

    Args:
        *dicts: Variable number of dictionaries to merge

    Returns:
        A new dictionary containing all key-value pairs
    """
    # Create an empty dictionary for the result
    result = {}

    # Iterate through each dictionary passed as argument
    # *dicts allows us to accept any number of dictionary arguments
    for d in dicts:
        # update() method adds all key-value pairs from one dict to another
        # If keys overlap, later values overwrite earlier ones
        result.update(d)

    return result


# Define the sample dictionaries
dic1 = {1: 10, 2: 20}
dic2 = {3: 30, 4: 40}
dic3 = {5: 50, 6: 60}

print("Concatenate dictionaries:")
print(f"dic1 = {dic1}")
print(f"dic2 = {dic2}")
print(f"dic3 = {dic3}")

# Method 1: Using our function
merged_dict = concatenate_dicts(dic1, dic2, dic3)
print(f"\nMerged (using function): {merged_dict}")

# Method 2: Using dictionary unpacking (Python 3.5+)
# The ** operator unpacks dictionary key-value pairs
merged_alt = {**dic1, **dic2, **dic3}
print(f"Merged (using ** unpacking): {merged_alt}")
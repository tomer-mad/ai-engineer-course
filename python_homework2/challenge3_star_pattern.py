"""
Challenge 3: Star Pattern (S-shape)
===================================
Task: Print a star pattern that forms an S shape.

Expected output:
****
*
*
 ***
    *
    *
****
"""


def print_s_pattern():
    """
    Print a star pattern that forms an S shape.

    The pattern has:
    - Row 1: 4 stars at the left (top of S)
    - Rows 2-3: 1 star at the left (left side going down)
    - Row 4: 3 stars (middle curve, indented by 1)
    - Rows 5-6: 1 star at the right (right side going down)
    - Row 7: 4 stars at the left (bottom of S)
    """
    # Define the pattern as a list of strings for clarity
    # This approach makes the pattern easy to visualize and modify
    pattern = [
        "****",      # Top of S
        "*",         # Left side going down
        "*",         # Left side going down
        " ***",      # Middle curve of S (indented)
        "    *",     # Right side going down (indented)
        "    *",     # Right side going down (indented)
        "****"       # Bottom of S
    ]

    # Print each line of the pattern
    for line in pattern:
        print(line)


def print_s_pattern_programmatic():
    """
    Print the S pattern using logic instead of hardcoded strings.
    This demonstrates how to build patterns programmatically.
    """
    width = 5  # Width of the pattern

    # Top horizontal line (4 stars)
    print("*" * 4)

    # Two rows with star on left
    for _ in range(2):
        print("*")

    # Middle line (3 stars, indented by 1)
    print(" " + "*" * 3)

    # Two rows with star on right
    for _ in range(2):
        print(" " * 4 + "*")

    # Bottom horizontal line (4 stars)
    print("*" * 4)


# Print using simple method
print("S-shape pattern (using list):")
print_s_pattern()

# Print using programmatic method
print("\nS-shape pattern (programmatic):")
print_s_pattern_programmatic()
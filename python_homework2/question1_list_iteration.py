"""
Question 1: Personal Information List with For Loop
===================================================
Task: Create a list with identification information and iterate through it
using a for loop to print each item.
"""

# Creating a list with personal identification information
# Lists in Python are ordered, mutable collections that can hold any data type
# We use square brackets [] to define a list
personal_info_list = ["Tomer", "Doe", 25, "tomer@email.com"]

# Using a for loop to iterate through the list
# The 'for' keyword lets us loop through each element in the list
# 'item' is a variable that takes the value of each element one by one
print("Personal Information:")
for item in personal_info_list:
    print(item)
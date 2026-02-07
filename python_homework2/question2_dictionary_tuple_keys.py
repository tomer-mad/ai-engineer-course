"""
Question 2: Personal Information Dictionary with Tuple Keys
===========================================================
Task: Create a dictionary with identification info using tuple keys where relevant.
Tuples are immutable (unchangeable) and can be used as dictionary keys.
"""

# Creating a dictionary with personal identification information
# Dictionaries store key-value pairs using curly braces {}
# Tuple keys (name, last_name) group related information together
personal_info_dict = {
    ("name", "last_name"): "Tomer Doe",  # Tuple key for full name
    "age": 25,                            # Simple string key for age
    "phone_number": "0527389001",         # Phone stored as string to preserve leading zeros
    "email": "tomer@email.com"            # Additional field
}

# Accessing values using their keys
print("Dictionary with tuple keys:")
print(f"Full name: {personal_info_dict[('name', 'last_name')]}")
print(f"Age: {personal_info_dict['age']}")
print(f"Phone: {personal_info_dict['phone_number']}")
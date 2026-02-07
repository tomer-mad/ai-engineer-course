"""
Titanic Ticket Booking System

This program allows users to purchase a ticket for the Titanic by:
1. Loading historical passenger data
2. Collecting passenger information
3. Validating all inputs
4. Assigning cabin class based on fare
5. Generating a unique ticket number
6. Calculating survival probability

REQUIRED FILE:
- titanic3.xls (historical Titanic passenger dataset)
  Expected location: Same directory as this Python script
  
If the file is not found, the program will prompt you to:
- Enter a different file name or path
- Exit and place the file in the correct location
"""

import random  # For generating random ticket numbers
import pandas as pd  # For reading and analyzing the Excel data
import os  # For file path operations

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Class assignment behavior when fare qualifies for multiple classes:
# 
# False (DEFAULT): "Step up one level" - More conservative, realistic pricing
#   Example: Fare $10 qualifies for 3rd, 2nd, AND 1st → Assigned to 2nd (one step up from 3rd)
#   
# True: "Jump to highest" - More generous, better survival odds  
#   Example: Fare $10 qualifies for 3rd, 2nd, AND 1st → Assigned to 1st (highest)
#
ALLOW_FULL_UPGRADE = False

# ==============================================================================
# STEP 1: LOAD AND ANALYZE HISTORICAL DATA
# ==============================================================================

print("Loading historical Titanic data...")

# Default file name - expected to be in the same directory as this script
DEFAULT_FILENAME = 'titanic3.xls'

# Try to load the historical Titanic passenger data from Excel file
df = None
data_file = DEFAULT_FILENAME

while df is None:
    try:
        df = pd.read_excel(data_file)
        print(f"✓ Successfully loaded {len(df)} historical passenger records")
        print(f"  from: {data_file}\n")
    except FileNotFoundError:
        print("\n" + "=" * 60)
        print("ERROR: Historical data file not found!")
        print("=" * 60)
        print(f"\nCould not find: '{data_file}'")
        print("\nThis file is REQUIRED to run the Titanic booking system.")
        print("The historical data is used to:")
        print("  • Validate fare ranges")
        print("  • Assign cabin classes")
        print("  • Prevent duplicate ticket numbers")
        print("  • Calculate survival probabilities")
        print("\n" + "-" * 60)
        print("Please choose an option:")
        print("  1. Enter a different file name or path")
        print("  2. Exit the program")
        print("-" * 60)
        
        choice = input("\nYour choice (1 or 2): ").strip()
        
        if choice == '1':
            data_file = input("\nEnter the file name or full path to titanic3.xls: ").strip()
            # Remove quotes if user copied a path with quotes
            data_file = data_file.strip('"').strip("'")
            print(f"\nAttempting to load: {data_file}...")
        elif choice == '2':
            print("\nExiting program. Please place 'titanic3.xls' in the same")
            print("directory as this script and try again.")
            exit()
        else:
            print("\nInvalid choice. Please enter 1 or 2.")
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR: Failed to read the data file!")
        print("=" * 60)
        print(f"\nFile found but could not be read: '{data_file}'")
        print(f"Error details: {str(e)}")
        print("\nPossible issues:")
        print("  • File may be corrupted")
        print("  • File may not be a valid Excel file")
        print("  • You may need to install openpyxl: pip install openpyxl")
        print("\n" + "-" * 60)
        print("Please choose an option:")
        print("  1. Try a different file")
        print("  2. Exit the program")
        print("-" * 60)
        
        choice = input("\nYour choice (1 or 2): ").strip()
        
        if choice == '1':
            data_file = input("\nEnter the file name or full path: ").strip()
            data_file = data_file.strip('"').strip("'")
            print(f"\nAttempting to load: {data_file}...")
        elif choice == '2':
            print("\nExiting program.")
            exit()
        else:
            print("\nInvalid choice. Exiting program.")
            exit()

# Extract all historical fares (removing any missing values and zeros)
# We exclude $0 fares because they don't represent real ticket prices
# (17 passengers had $0 fare, likely crew members or special cases)
all_fares = df[df['fare'] > 0]['fare'].dropna()

# Calculate minimum and maximum fares across all passengers
MIN_FARE = all_fares.min()  # Lowest fare ever paid: $3.17
MAX_FARE = all_fares.max()  # Highest fare ever paid: $512.33

# Analyze fare ranges for each class (excluding $0 fares)
# This helps us assign passengers to the correct class based on what they pay
first_class_fares = df[(df['pclass'] == 1) & (df['fare'] > 0)]['fare'].dropna()
second_class_fares = df[(df['pclass'] == 2) & (df['fare'] > 0)]['fare'].dropna()
third_class_fares = df[(df['pclass'] == 3) & (df['fare'] > 0)]['fare'].dropna()

FIRST_CLASS_MIN = first_class_fares.min()
FIRST_CLASS_MAX = first_class_fares.max()

SECOND_CLASS_MIN = second_class_fares.min()
SECOND_CLASS_MAX = second_class_fares.max()

THIRD_CLASS_MIN = third_class_fares.min()
THIRD_CLASS_MAX = third_class_fares.max()

# Print the fare ranges for reference
print("=" * 60)
print("TITANIC TICKET BOOKING SYSTEM")
print("=" * 60)
print(f"\nFare Information:")
print(f"Valid fare range: ${MIN_FARE:.2f} - ${MAX_FARE:.2f}")
print(f"1st Class: ${FIRST_CLASS_MIN:.2f} - ${FIRST_CLASS_MAX:.2f}")
print(f"2nd Class: ${SECOND_CLASS_MIN:.2f} - ${SECOND_CLASS_MAX:.2f}")
print(f"3rd Class: ${THIRD_CLASS_MIN:.2f} - ${THIRD_CLASS_MAX:.2f}")
print(f"\nNote: $0 fares excluded from range calculation")
print()

# Extract all historical ticket numbers
# We'll check against these to avoid duplicates
historical_tickets = set()
for ticket in df['ticket'].dropna():
    try:
        # Try to convert ticket to integer (some tickets are strings)
        ticket_num = int(str(ticket).strip())
        # Only store 6-digit tickets
        if 100000 <= ticket_num <= 999999:
            historical_tickets.add(ticket_num)
    except:
        # Skip non-numeric tickets
        pass

print(f"Found {len(historical_tickets)} historical 6-digit ticket numbers")

# Store newly issued ticket numbers to prevent duplicates
issued_tickets = set()

# Calculate survival statistics from historical data
# These will be used to estimate new passenger's survival chances

# Survival rate by class
class1_survival = df[df['pclass'] == 1]['survived'].mean()
class2_survival = df[df['pclass'] == 2]['survived'].mean()
class3_survival = df[df['pclass'] == 3]['survived'].mean()

# Survival rate by sex
male_survival = df[df['sex'] == 'male']['survived'].mean()
female_survival = df[df['sex'] == 'female']['survived'].mean()

# Survival rate by age group
children_survival = df[df['age'] < 16]['survived'].mean()
adults_survival = df[(df['age'] >= 16) & (df['age'] < 60)]['survived'].mean()
elderly_survival = df[df['age'] >= 60]['survived'].mean()

print(f"\nHistorical Survival Rates:")
print(f"1st Class: {class1_survival*100:.1f}%")
print(f"2nd Class: {class2_survival*100:.1f}%")
print(f"3rd Class: {class3_survival*100:.1f}%")
print(f"Male: {male_survival*100:.1f}%")
print(f"Female: {female_survival*100:.1f}%")
print()

# ==============================================================================
# STEP 2: DEFINE HELPER FUNCTIONS
# ==============================================================================

def get_valid_fare():
    """
    Get and validate fare from user.
    Keep asking until a valid fare is entered.
    
    Returns:
        float: A valid fare amount
    """
    while True:  # Loop forever until we get valid input
        # Get fare as a string from user
        fare_str = input("Enter fare amount: $")
        
        try:
            # Try to convert string to float
            fare = float(fare_str)
            
            # Check if fare is within valid range
            if MIN_FARE <= fare <= MAX_FARE:
                return fare  # Valid fare! Return it and exit function
            else:
                # Fare is outside valid range
                print("Your fare payment is illegal. Please pay again.")
                print(f"Fare must be between ${MIN_FARE:.2f} and ${MAX_FARE:.2f}")
        except ValueError:
            # User entered something that can't be converted to a number
            print("Invalid input. Please enter a number.")


def get_valid_age():
    """
    Get and validate age from user.
    Keep asking until a valid age is entered.
    
    Returns:
        float: A valid age
    """
    while True:  # Loop forever until we get valid input
        # Get age as a string from user
        age_str = input("Enter your age: ")
        
        try:
            # Try to convert string to float
            age = float(age_str)
            
            # Check if age is within valid range (0 to 130)
            if 0 <= age <= 130:
                return age  # Valid age! Return it and exit function
            else:
                # Age is outside valid range
                print("Your age is wrong. Please enter your age again.")
                print("Age must be between 0 and 130.")
        except ValueError:
            # User entered something that can't be converted to a number
            print("Invalid input. Please enter a number.")


def get_valid_sex():
    """
    Get and validate gender from user.
    Keep asking until a valid gender is entered.
    
    Returns:
        str: Either 'male' or 'female'
    """
    while True:  # Loop forever until we get valid input
        # Get sex as a string from user
        sex = input("Enter your sex (male/female): ")
        
        # Convert to lowercase to make comparison case-insensitive
        sex = sex.lower().strip()
        
        # Check if sex is either 'male' or 'female'
        if sex == 'male' or sex == 'female':
            return sex  # Valid gender! Return it and exit function
        else:
            # Invalid gender
            print("The sex value is illegal. Please enter again.")
            print("Please enter 'male' or 'female'.")


def get_valid_name():
    """
    Get and validate passenger name from user.
    Keep asking until a valid name is entered.
    
    Valid name requirements:
    - At least 2 characters long (after removing leading/trailing spaces)
    - Must contain at least one letter (not just spaces, numbers, or symbols)
    - Cannot be empty or only whitespace
    
    Returns:
        str: A valid name (with leading/trailing spaces removed)
    """
    while True:  # Loop forever until we get valid input
        # Get name as a string from user
        name = input("Enter your name: ")
        
        # Remove leading and trailing spaces
        name = name.strip()
        
        # Check if name is empty or only whitespace
        if len(name) == 0:
            print("Name cannot be empty. Please enter your name.")
            continue
        
        # Check if name is at least 2 characters long
        if len(name) < 2:
            print("Name must be at least 2 characters long. Please enter your full name.")
            continue
        
        # Check if name contains at least one letter (not just numbers/symbols/spaces)
        has_letter = False
        for char in name:
            if char.isalpha():  # Check if character is a letter
                has_letter = True
                break
        
        if not has_letter:
            print("Name must contain at least one letter. Please enter a valid name.")
            continue
        
        # All checks passed! Name is valid
        return name


def assign_cabin_class(fare, allow_full_upgrade=False):
    """
    Determine which cabin class the passenger gets based on their fare.
    
    DEFAULT BEHAVIOR (allow_full_upgrade=False):
    Step up ONE LEVEL from the base class when fare qualifies for multiple classes.
    - If fare qualifies for 3rd class only → 3rd class
    - If fare qualifies for 3rd AND 2nd → 2nd class (step up once)
    - If fare qualifies for 3rd, 2nd, AND 1st → 2nd class (step up once from 3rd)
    - If fare qualifies for 2nd AND 1st → 1st class (step up once from 2nd)
    - If fare qualifies for 1st only → 1st class
    
    ALTERNATIVE BEHAVIOR (allow_full_upgrade=True):
    Assign to HIGHEST class when fare qualifies for multiple classes.
    - If fare qualifies for multiple classes → Always assign to highest qualifying class
    - This gives better survival odds but may not reflect realistic pricing
    
    Historical fare ranges (excluding $0):
    - 1st Class: $5.00 - $512.33
    - 2nd Class: $9.69 - $73.50
    - 3rd Class: $3.17 - $69.55
    
    OVERLAP ZONES (DEFAULT):
    - $9.69 - $69.55: ALL THREE classes overlap → Assign to 2nd (one step up from 3rd)
    - $69.56 - $73.50: 1st and 2nd classes overlap → Assign to 1st (one step up from 2nd)
    - $5.00 - $9.68: 1st and 3rd overlap → Assign to 1st (can't step to 2nd, not qualified)
    
    OVERLAP ZONES (allow_full_upgrade=True):
    - $9.69 - $69.55: ALL THREE classes overlap → Assign to 1st (highest)
    - $69.56 - $73.50: 1st and 2nd classes overlap → Assign to 1st (highest)
    - $5.00 - $9.68: 1st and 3rd overlap → Assign to 1st (highest)
    
    EXAMPLES (DEFAULT):
    - Fare $10: Qualifies for 1st, 2nd, AND 3rd → Assigned to 2nd (step up from 3rd)
    - Fare $70: Qualifies for 1st and 2nd → Assigned to 1st (step up from 2nd)
    - Fare $8: Qualifies for 1st and 3rd (not 2nd) → Assigned to 1st (no 2nd option)
    - Fare $400: Qualifies for 1st only → Assigned to 1st
    
    EXAMPLES (allow_full_upgrade=True):
    - Fare $10: Qualifies for 1st, 2nd, AND 3rd → Assigned to 1st (highest)
    - Fare $70: Qualifies for 1st and 2nd → Assigned to 1st (highest)
    - Fare $8: Qualifies for 1st and 3rd → Assigned to 1st (highest)
    - Fare $400: Qualifies for 1st only → Assigned to 1st
    
    Args:
        fare (float): The amount the passenger paid
        allow_full_upgrade (bool): If True, assign to highest qualifying class.
                                   If False (default), step up one level only.
        
    Returns:
        int: The cabin class (1, 2, or 3)
    """
    # Check which classes the fare qualifies for
    qualifies_for_first = FIRST_CLASS_MIN <= fare <= FIRST_CLASS_MAX
    qualifies_for_second = SECOND_CLASS_MIN <= fare <= SECOND_CLASS_MAX
    qualifies_for_third = THIRD_CLASS_MIN <= fare <= THIRD_CLASS_MAX
    
    # ALTERNATIVE MODE: Assign to highest qualifying class
    if allow_full_upgrade:
        # Simply check from highest to lowest, first match wins
        if qualifies_for_first:
            return 1
        elif qualifies_for_second:
            return 2
        elif qualifies_for_third:
            return 3
        else:
            # Handle edge cases for fares outside all ranges
            if fare > FIRST_CLASS_MAX:
                return 1
            elif fare > SECOND_CLASS_MAX:
                return 2
            else:
                return 3
    
    # DEFAULT MODE: Apply "step up one level" logic
    else:
        if qualifies_for_third:
            # Base class is 3rd
            if qualifies_for_second:
                # Can step up to 2nd class
                return 2
            elif qualifies_for_first:
                # Qualifies for 1st but not 2nd (rare edge case)
                # Step up to 1st since 2nd is not an option
                return 1
            else:
                # Only qualifies for 3rd
                return 3
        
        elif qualifies_for_second:
            # Base class is 2nd (doesn't qualify for 3rd)
            if qualifies_for_first:
                # Can step up to 1st class
                return 1
            else:
                # Only qualifies for 2nd
                return 2
        
        elif qualifies_for_first:
            # Only qualifies for 1st class
            return 1
        
        # Handle edge cases for fares outside all ranges
        else:
            if fare > FIRST_CLASS_MAX:
                return 1  # Very high fare -> 1st class
            elif fare > SECOND_CLASS_MAX:
                return 2  # Medium-high fare -> 2nd class
            else:
                return 3  # Low fare -> 3rd class


def generate_unique_ticket_number():
    """
    Generate a unique 6-digit ticket number.
    Keep generating until we find one that hasn't been used historically
    or issued in this session.
    
    Returns:
        str: A unique 6-digit ticket number
    """
    while True:  # Loop until we find a unique number
        # Generate a random 6-digit number (100000 to 999999)
        ticket_number = random.randint(100000, 999999)
        
        # Check if this ticket number exists in historical data
        # OR has already been issued in this session
        if ticket_number not in historical_tickets and ticket_number not in issued_tickets:
            # This number is unique! Add it to our issued set and return it
            issued_tickets.add(ticket_number)
            return str(ticket_number)  # Convert to string for easier handling


def calculate_survival_probability(name, age, sex, fare, cabin_class):
    """
    Calculate the probability of death based on passenger characteristics.
    This uses actual historical statistics from the Titanic dataset with a 
    minimum sample size of 20 people for statistical significance.
    
    The calculation:
    1. Filters historical data by cabin class and sex (exact match)
    2. Creates an age range around the passenger's age (±10 years initially)
    3. Expands the age range until at least 20 similar passengers are found
    4. Calculates survival rate from this matched group
    
    Args:
        name (str): Passenger name
        age (float): Passenger age
        sex (str): Passenger gender
        fare (float): Fare paid
        cabin_class (int): Assigned cabin class
        
    Returns:
        float: Death probability as a percentage
    """
    # Filter historical data by class and sex (these must match exactly)
    similar_passengers = df[(df['pclass'] == cabin_class) & (df['sex'] == sex)].copy()
    
    # Remove passengers with missing age data
    similar_passengers = similar_passengers[similar_passengers['age'].notna()]
    
    # If we don't have enough data for this class/sex combination, use broader criteria
    if len(similar_passengers) < 20:
        # Fall back to just class-based calculation
        similar_passengers = df[df['pclass'] == cabin_class].copy()
        similar_passengers = similar_passengers[similar_passengers['age'].notna()]
    
    # Start with age range of ±10 years
    age_range = 10
    matched_group = None
    
    # Keep expanding age range until we have at least 20 people
    # Maximum expansion to ±50 years to ensure we eventually get 20 people
    while age_range <= 50:
        # Calculate age bounds
        min_age = max(0, age - age_range)  # Don't go below 0
        max_age = min(130, age + age_range)  # Don't go above 130
        
        # Filter by age range
        matched_group = similar_passengers[
            (similar_passengers['age'] >= min_age) & 
            (similar_passengers['age'] <= max_age)
        ]
        
        # Check if we have enough people
        if len(matched_group) >= 20:
            break
        
        # Expand the range by 5 years on each side
        age_range += 5
    
    # If still not enough people (very rare), use all available similar passengers
    if matched_group is None or len(matched_group) < 20:
        matched_group = similar_passengers
    
    # Calculate survival rate from the matched group
    if len(matched_group) > 0:
        survival_rate = matched_group['survived'].mean()
        sample_size = len(matched_group)
    else:
        # Emergency fallback: use overall class survival rate
        survival_rate = df[df['pclass'] == cabin_class]['survived'].mean()
        sample_size = len(df[df['pclass'] == cabin_class])
    
    # Convert survival rate to death probability
    death_probability = (1 - survival_rate) * 100
    
    # Make sure probability stays between 0 and 100
    death_probability = max(0.0, min(100.0, death_probability))
    
    # Print debug information (optional - can be commented out)
    print(f"\nSurvival calculation based on {sample_size} historical passengers:")
    print(f"  Age range: {max(0, age - age_range):.0f} - {min(130, age + age_range):.0f} years")
    print(f"  Class: {cabin_class}, Sex: {sex}")
    print(f"  Historical survival rate: {survival_rate*100:.1f}%")
    
    return death_probability


def save_ticket_to_file(name, age, sex, fare, cabin_class, ticket_number):
    """
    Save the passenger ticket information to a text file.
    
    Args:
        name (str): Passenger name
        age (float): Passenger age
        sex (str): Passenger gender
        fare (float): Fare paid
        cabin_class (int): Assigned cabin class
        ticket_number (str): Unique ticket number
    """
    # Create a filename using the ticket number
    filename = f"ticket_{ticket_number}.txt"
    
    # Open file for writing (creates new file or overwrites existing)
    with open(filename, 'w') as file:
        # Write passenger information in a formatted way
        file.write("=" * 50 + "\n")
        file.write("TITANIC PASSENGER TICKET\n")
        file.write("=" * 50 + "\n\n")
        file.write(f"Name: {name}\n")
        file.write(f"Age: {age}\n")
        file.write(f"Sex: {sex.capitalize()}\n")
        file.write(f"Fare: ${fare:.2f}\n")
        file.write(f"Class: {cabin_class}\n")
        file.write(f"Ticket Number: {ticket_number}\n")
        file.write("\n" + "=" * 50 + "\n")
        file.write("Thank you for choosing RMS Titanic!\n")
        file.write("=" * 50 + "\n")
    
    print(f"\nTicket saved to {filename}")


# ==============================================================================
# STEP 3: MAIN PROGRAM
# ==============================================================================

def main():
    """
    Main function that runs the entire ticket booking process.
    """
    print("=" * 60)
    print("Welcome to Titanic Ticket Booking!")
    print("=" * 60)
    print()
    
    # Step 1: Get and validate passenger name
    name = get_valid_name()
    print()
    
    # Step 2: Get and validate age
    age = get_valid_age()
    print()
    
    # Step 3: Get and validate fare
    fare = get_valid_fare()
    print()
    
    # Step 4: Get and validate sex
    sex = get_valid_sex()
    print()
    
    # Step 5: Assign cabin class based on fare
    cabin_class = assign_cabin_class(fare, allow_full_upgrade=ALLOW_FULL_UPGRADE)
    print(f"Based on your fare of ${fare:.2f}, you are assigned to Class {cabin_class}")
    
    # Show upgrade information if fare qualifies for multiple classes
    if cabin_class == 2 and not ALLOW_FULL_UPGRADE:
        # Check if it would have been 1st class with full upgrade
        first_class_min = df[(df['pclass'] == 1) & (df['fare'] > 0)]['fare'].min()
        first_class_max = df[(df['pclass'] == 1) & (df['fare'] > 0)]['fare'].max()
        if first_class_min <= fare <= first_class_max:
            print(f"  (Your fare qualifies for 1st class too, but 2nd class is assigned)")
    
    print()
    
    # Step 6: Generate unique ticket number
    ticket_number = generate_unique_ticket_number()
    print(f"Your ticket number is: {ticket_number}")
    print()
    
    # Step 7: Calculate survival probability
    death_probability = calculate_survival_probability(name, age, sex, fare, cabin_class)
    
    # Step 8: Display survival message
    print("=" * 60)
    print(f"Dear {name}, your chances to die on our trip are {death_probability:.1f}%.")
    print("Enjoy your trip ☺")
    print("=" * 60)
    print()
    
    # Step 9: Save ticket to file
    save_ticket_to_file(name, age, sex, fare, cabin_class, ticket_number)
    
    print("\nThank you for booking with Titanic!")


# ==============================================================================
# RUN THE PROGRAM
# ==============================================================================

# This check ensures the code only runs if this file is run directly
# (not when it's imported as a module in another program)
if __name__ == "__main__":
    main()

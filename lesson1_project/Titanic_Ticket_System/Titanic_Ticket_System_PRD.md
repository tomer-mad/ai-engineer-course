# Product Requirements Document
# Titanic Ticket Booking System

**Version:** 1.0  
**Date:** January 30, 2026  
**Owner:** Development Team

---

## 1. Overview

This document outlines the requirements for a Titanic ticket booking and survival prediction system. The system will validate passenger information, assign cabin classes based on fare, generate unique ticket numbers, and calculate survival probability.

---

## 2. Objectives

- Create a robust input validation system for passenger data
- Implement dynamic fare-based cabin class assignment
- Generate unique 6-digit ticket numbers
- Calculate and display survival probability
- Save passenger ticket information to a text file

---

## 3. Functional Requirements

### 3.1 Input Collection

The system must collect the following passenger information via input function:

- **name** (string): Passenger's full name
- **age** (float): Passenger's age in years
- **fare** (float): Amount paid for the ticket
- **sex** (string): Passenger's gender (male/female)

**Note:** All inputs are received as strings. The system must convert age and fare to float using appropriate type conversion functions.

---

### 3.2 Data Validation

#### 3.2.1 Fare Validation

1. Calculate the minimum fare from historical passenger data
2. Calculate the maximum fare from historical passenger data
3. Validate that entered fare is within [min_fare, max_fare] range
4. If invalid: display error message and prompt user to re-enter fare

**Error message:** "Your fare payment is illegal. Please pay again."

#### 3.2.2 Age Validation

1. Validate that age is between 0 and 130 (inclusive)
2. If invalid: display error message and prompt user to re-enter age
3. Repeat validation until valid age is received

**Error message:** "Your age is wrong. Please enter your age again."

#### 3.2.3 Gender Validation

1. Validate that sex value is either 'male' or 'female' (case-insensitive)
2. If invalid: display error message and prompt user to re-enter sex
3. Repeat validation until valid value is received

**Error message:** "The sex value is illegal. Please enter again."

#### 3.2.4 Name Processing

Remove leading and trailing whitespace from the name using the strip() method or equivalent.

---

### 3.3 Cabin Class Assignment

The system must determine cabin class based on the fare paid:

1. Analyze historical data to determine fare ranges for each class (1st, 2nd, 3rd)
2. Find minimum and maximum fare for each cabin class
3. When passenger's fare falls into overlapping ranges, assign to the higher class
4. Store assigned class for ticket generation

**Example:** If 1st class range is [$100-$300] and 2nd class range is [$50-$200], a fare of $175 assigns the passenger to 1st class (higher priority).

---

### 3.4 Ticket Number Generation

1. Generate a random 6-digit ticket number
2. Check if the generated number already exists in the system
3. If duplicate detected, regenerate until unique number is found
4. Store the ticket number to prevent future duplicates

---

### 3.5 Ticket File Output

Write passenger information to a text file with the following format:

| Field | Description |
|-------|-------------|
| Name | Passenger's cleaned name |
| Age | Validated age value |
| Sex | Validated gender value |
| Fare | Validated fare amount |
| Class | Assigned cabin class (1, 2, or 3) |
| Ticket Number | Unique 6-digit number |

---

### 3.6 Survival Probability Calculation

1. Filter historical passengers by exact match: cabin class AND gender
2. Start with age range of ±10 years from passenger's age
3. Count passengers in the filtered group within the age range
4. If fewer than 20 passengers found:
   - Expand age range by ±5 years
   - Repeat until at least 20 passengers found (up to ±50 years maximum)
5. Calculate survival rate from the matched group of similar passengers
6. Display result as a percentage with one decimal place
7. Format output message for user notification

**Minimum Sample Size Rule:**
- Statistical calculations require at least 20 similar passengers
- Age range dynamically expands until this threshold is met
- Example: Age 50 starts with range 40-60, expands to 35-65, then 30-70, etc. until 20+ passengers found

**Matching Criteria Priority:**
1. **Exact match**: Class + Gender + Age range (±10 years initially)
2. **If < 20 people**: Expand age range in 5-year increments
3. **Fallback**: If still insufficient, use all passengers in same class

**Output format:** "Dear [Name], your chances to die on our trip are [XX.X]%. Enjoy your trip ☺"

**Example:** "Dear Alex, your chances to die on our trip are 73.7%. Enjoy your trip ☺"

**Debug Information Displayed:**
- Number of historical passengers in sample
- Age range used for calculation
- Class and gender filters applied
- Historical survival rate of the matched group

---

## 4. Technical Requirements

### 4.1 Data Sources

- Access to historical Titanic passenger dataset
- Dataset must include: passenger class, fare amounts, survival outcomes, age, sex
- Recommend using the Kaggle Titanic dataset or equivalent source

### 4.2 Programming Requirements

- Use input() function for all user data collection
- Implement type conversion: string to float for age and fare
- Implement validation loops with error messages and re-prompting
- Use random number generation for ticket numbers
- Implement duplicate detection for ticket numbers
- File I/O operations for ticket writing
- Statistical analysis for survival probability calculation

### 4.3 Data Structures

- Maintain a collection of issued ticket numbers to prevent duplicates
- Store fare range boundaries for each cabin class
- Maintain survival statistics indexed by relevant passenger attributes

---

## 5. Implementation Workflow

### 1. Data Preparation Phase
   - Load historical Titanic dataset
   - Calculate min/max fare values across all passengers
   - Determine fare ranges for each cabin class
   - Calculate survival statistics by demographic groups

### 2. Input Collection Phase
   - Prompt for name, age, fare, sex
   - Convert string inputs to appropriate types

### 3. Validation Phase
   - Validate fare against min/max bounds
   - Validate age is between 0-130
   - Validate sex is male or female
   - Clean name (strip whitespace)

### 4. Processing Phase
   - Assign cabin class based on fare
   - Generate unique ticket number
   - Calculate survival probability

### 5. Output Phase
   - Write ticket information to text file
   - Display survival probability message to user

---

## 6. Acceptance Criteria

- System rejects fares outside the historical min-max range
- System rejects ages outside 0-130 range
- System rejects sex values other than 'male' or 'female'
- System re-prompts user after each validation failure until valid input received
- Names are properly cleaned of leading/trailing whitespace
- Cabin class is correctly assigned with preference for higher class in overlapping ranges
- Ticket numbers are always 6 digits and unique
- Ticket file contains all required fields in specified format
- Survival probability is calculated and displayed with proper formatting
- Death probability message includes passenger name and percentage

---

## 7. Edge Cases and Considerations

- **Fare at exact boundaries:** Handle fares that equal min or max values
- **Class overlap:** When fare qualifies for multiple classes, always assign to higher class
- **Ticket number exhaustion:** Consider what happens if all 1,000,000 possible 6-digit numbers are used
- **Case sensitivity:** Sex validation should be case-insensitive
- **Empty names:** Consider handling names that become empty after stripping
- **Float precision:** Handle age and fare with appropriate decimal precision

---

## 8. Deliverables

1. Working Python program implementing all requirements
2. Documentation explaining the survival probability calculation methodology
3. Test cases demonstrating validation logic
4. Sample output file showing ticket format

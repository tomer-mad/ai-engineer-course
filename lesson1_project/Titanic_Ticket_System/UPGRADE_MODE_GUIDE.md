# Cabin Class Assignment - Configuration Guide

## Overview

The Titanic Ticket System now supports **two modes** for assigning cabin classes when a fare qualifies for multiple classes.

You can control this behavior by setting the `ALLOW_FULL_UPGRADE` flag at the top of `titanic_ticket_system.py`.

---

## Configuration

Open `titanic_ticket_system.py` and find this line near the top:

```python
# Line ~37
ALLOW_FULL_UPGRADE = False  # Change this to True for different behavior
```

---

## Mode 1: Step Up One Level (DEFAULT)

**Setting**: `ALLOW_FULL_UPGRADE = False`

### Behavior:
When a fare qualifies for multiple classes, the passenger gets **one level upgrade** from the lowest qualifying class.

### Examples:

| Fare | Qualifies For | Assigned Class | Reasoning |
|------|---------------|----------------|-----------|
| $10 | 3rd + 2nd + 1st | **2nd Class** | Step up once from 3rd |
| $50 | 3rd + 2nd + 1st | **2nd Class** | Step up once from 3rd |
| $70 | 2nd + 1st | **1st Class** | Step up once from 2nd |
| $100 | 1st only | **1st Class** | Only option |

### Test Result (Fare $50):
```
Based on your fare of $50.00, you are assigned to Class 2
  (Your fare qualifies for 1st class too, but 2nd class is assigned)

Survival calculation based on 97 historical passengers:
  Class: 2, Sex: male
  Historical survival rate: 9.3%
  
Dear Test Person, your chances to die on our trip are 90.7%.
```

### Why Use This Mode?

✅ **More realistic pricing** - A $10 ticket shouldn't get luxury treatment  
✅ **Conservative upgrade** - Reflects budget vs premium cabins  
✅ **Fairer distribution** - Lower fares get appropriate class  
✅ **Historical accuracy** - Better matches actual passenger experiences  

**Use when**: You want realistic, conservative class assignments

---

## Mode 2: Jump to Highest Class

**Setting**: `ALLOW_FULL_UPGRADE = True`

### Behavior:
When a fare qualifies for multiple classes, the passenger gets assigned to the **highest** qualifying class.

### Examples:

| Fare | Qualifies For | Assigned Class | Reasoning |
|------|---------------|----------------|-----------|
| $10 | 3rd + 2nd + 1st | **1st Class** | Highest qualifying |
| $50 | 3rd + 2nd + 1st | **1st Class** | Highest qualifying |
| $70 | 2nd + 1st | **1st Class** | Highest qualifying |
| $100 | 1st only | **1st Class** | Only option |

### Test Result (Fare $50):
```
Based on your fare of $50.00, you are assigned to Class 1

Survival calculation based on 62 historical passengers:
  Class: 1, Sex: male
  Historical survival rate: 41.9%
  
Dear Test Person, your chances to die on our trip are 58.1%.
```

### Why Use This Mode?

✅ **Better survival odds** - Higher class = better survival rates  
✅ **More generous** - Passengers get maximum value  
✅ **Simpler logic** - Easy to understand  
✅ **Original behavior** - How the system worked initially  

**Use when**: You want to maximize passenger benefits and survival odds

---

## Comparison

### Fare $50 Example:

| Metric | Step Up (False) | Jump to Highest (True) | Difference |
|--------|-----------------|------------------------|------------|
| **Assigned Class** | 2nd Class | 1st Class | Higher class |
| **Survival Rate** | 9.3% | 41.9% | +32.6% |
| **Death Probability** | 90.7% | 58.1% | -32.6% |
| **Sample Size** | 97 passengers | 62 passengers | Different pool |

**Same fare, dramatically different outcomes!**

---

## How to Change the Setting

### Step 1: Open the file
```bash
# Open in your text editor
nano titanic_ticket_system.py
# or
code titanic_ticket_system.py
# or open in any text editor
```

### Step 2: Find the configuration section
Look for this around line 37:

```python
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
```

### Step 3: Change the value
```python
# For "step up one level" mode (DEFAULT):
ALLOW_FULL_UPGRADE = False

# For "jump to highest" mode:
ALLOW_FULL_UPGRADE = True
```

### Step 4: Save and run
```bash
python titanic_ticket_system.py
```

---

## Which Mode Should You Use?

### Use `False` (Step Up One Level) if you want:
- ✅ More realistic, conservative assignments
- ✅ Fairer pricing structure
- ✅ Historical accuracy
- ✅ Budget fares don't get luxury treatment

### Use `True` (Jump to Highest) if you want:
- ✅ Maximum passenger benefits
- ✅ Best possible survival odds
- ✅ Simpler "higher class wins" logic
- ✅ More generous upgrade policy

---

## Impact Analysis

### Fares Affected by the Change:

Only fares in **overlap zones** are affected:

| Fare Range | Qualifies For | Class (False) | Class (True) |
|------------|---------------|---------------|--------------|
| $5.00 - $9.68 | 1st + 3rd | 1st | 1st (same) |
| $9.69 - $69.55 | **ALL THREE** | **2nd** | **1st** ⚠️ |
| $69.56 - $73.50 | 1st + 2nd | 1st | 1st (same) |
| $73.51+ | 1st only | 1st | 1st (same) |

**Main impact**: Fares between $9.69-$69.55 get different classes

### Percentage of Passengers Affected:

From historical data:
- **~12% of all passengers** paid in the $10-$70 range
- These passengers experience different class assignments
- All other passengers unaffected

---

## Technical Details

### Function Signature:
```python
def assign_cabin_class(fare, allow_full_upgrade=False):
    """
    Determine which cabin class the passenger gets based on their fare.
    
    Args:
        fare (float): The amount the passenger paid
        allow_full_upgrade (bool): If True, assign to highest qualifying class.
                                   If False (default), step up one level only.
    
    Returns:
        int: The cabin class (1, 2, or 3)
    """
```

### Implementation:
The function checks which classes the fare qualifies for, then:

**If `allow_full_upgrade=False` (default)**:
- Starts from lowest qualifying class
- Steps up one level if possible
- Example: 3rd → 2nd (not 3rd → 1st)

**If `allow_full_upgrade=True`**:
- Checks from highest to lowest
- First match wins
- Example: Qualifies for 1st → assign 1st

---

## Jupyter Notebook Version

If using the `.ipynb` file, the flag is also available. Look for the same configuration section in the first code cell after setup.

---

## Questions?

**Q: Does this affect survival probability?**  
A: Yes! Higher class = better survival odds. With `True`, overlap-zone passengers get better survival rates.

**Q: Which is historically accurate?**  
A: `False` (step up) is more realistic. A $10 ticket wouldn't get the same treatment as $200.

**Q: Can I change this while the program is running?**  
A: No, you need to edit the file and restart the program.

**Q: What's the default?**  
A: `False` (step up one level) - more conservative and realistic.

---

## Summary

| Feature | Step Up (False) | Jump to Highest (True) |
|---------|----------------|------------------------|
| **Default** | ✅ Yes | No |
| **Realistic** | ✅ More | Less |
| **Generous** | Less | ✅ More |
| **Survival Odds** | Lower | ✅ Higher |
| **Complexity** | Slightly more | ✅ Simpler |
| **Recommended For** | Educational accuracy | Passenger benefit |

**Default recommendation**: Keep `ALLOW_FULL_UPGRADE = False` for realistic simulation.

**Change to** `True` if you want to maximize passenger survival odds and provide more generous upgrades.

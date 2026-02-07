# Titanic Ticket Booking System

## Quick Start Guide

**Choose your preferred method:**

| Method | Best For | Setup Time | Difficulty |
|--------|----------|------------|------------|
| Google Colab | Beginners, no installation | 2 minutes | ⭐ Easy |
| Local Python | Those with Python installed | 5 minutes | ⭐⭐ Medium |
| Jupyter Notebook | Data scientists, analysts | 5 minutes | ⭐⭐ Medium |
| VSCode | Developers | 5 minutes | ⭐⭐⭐ Advanced |

**Absolute Beginner?** → Use **Google Colab** (no installation needed!)

## Overview
This system simulates booking a ticket for the Titanic using historical passenger data. It validates passenger information, assigns cabin classes, generates unique ticket numbers, and calculates survival probability.

### ⚙️ NEW: Configurable Class Assignment

You can now control how cabin classes are assigned when a fare qualifies for multiple classes!

Edit `titanic_ticket_system.py` line ~37:
```python
ALLOW_FULL_UPGRADE = False  # Default: Step up one level (realistic)
# Change to True for: Jump to highest class (generous)
```

**Example with $50 fare**:
- `False` → 2nd class (one level up from 3rd) - 90.7% death rate
- `True` → 1st class (highest qualifying) - 58.1% death rate

📖 See `UPGRADE_MODE_GUIDE.md` for complete details.

## Files Included
1. **titanic_ticket_system.py** - Main Python program (for local use)
2. **titanic_ticket_system.ipynb** - Jupyter Notebook version (for Colab/Jupyter)
3. **titanic3.xls** - Historical Titanic passenger dataset (1309 passengers)
4. **requirements.txt** - Python dependencies
5. **Titanic_Ticket_System_PRD.md** - Product Requirements Document
6. **README.md** - This file

## Requirements
- Python 3.x
- pandas library (for reading Excel files)
- openpyxl library (for Excel support)

## Installation & Setup

### Option 1: Local Python (Recommended for beginners)

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Install required libraries**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install pandas openpyxl
   ```
   
   If using `pip3`:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Place files in the same directory**:
   - titanic_ticket_system.py
   - titanic3.xls

4. **Run the program**:
   ```bash
   python titanic_ticket_system.py
   ```
   
   Or:
   ```bash
   python3 titanic_ticket_system.py
   ```

### Option 2: Google Colab (No installation needed!)

1. **Go to [Google Colab](https://colab.research.google.com/)**

2. **Upload the notebook**:
   - Click "File" → "Upload notebook"
   - Upload `titanic_ticket_system.ipynb`

3. **Upload the data file**:
   - Click the folder icon on the left sidebar
   - Click the upload button
   - Upload `titanic3.xls`

4. **Run all cells**:
   - Click "Runtime" → "Run all"
   - Or press Ctrl+F9 (Cmd+F9 on Mac)

5. **Follow the prompts** in the last cell to book your ticket

**Google Colab Advantages**:
- ✓ No installation required
- ✓ Works on any device with a browser
- ✓ Free GPU/TPU access (not needed for this project)
- ✓ Libraries auto-install

### Option 3: Jupyter Notebook (Local)

1. **Install Jupyter**:
   ```bash
   pip install jupyter notebook
   ```
   
   Or:
   ```bash
   pip3 install jupyter notebook
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Place files in the same directory**:
   - titanic_ticket_system.ipynb
   - titanic3.xls

4. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

5. **In the browser**:
   - Click on `titanic_ticket_system.ipynb`
   - Run all cells (Cell → Run All)
   - Follow the prompts in the last cell

### Option 4: VSCode with Jupyter Extension

1. **Install VSCode** from [code.visualstudio.com](https://code.visualstudio.com/)

2. **Install Python extension**:
   - Click Extensions icon (or Ctrl+Shift+X)
   - Search "Python"
   - Install the Microsoft Python extension

3. **Install Jupyter extension**:
   - Search "Jupyter" in Extensions
   - Install the Microsoft Jupyter extension

4. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Open the notebook**:
   - Open `titanic_ticket_system.ipynb` in VSCode
   - Click "Run All" at the top
   - Follow the prompts

## Usage

The program will prompt you for:
1. **Name** - Your full name
2. **Age** - Must be between 0 and 130
3. **Fare** - Must be between $3.17 and $512.33 (historical range, excluding $0 fares)
4. **Sex** - Either 'male' or 'female'

### Validation Rules
- **Fare**: Must be within the historical range found in the dataset
- **Age**: Must be between 0 and 130
- **Sex**: Must be 'male' or 'female' (case-insensitive)
- **Name**: Leading/trailing spaces are automatically removed

The program will re-prompt you if any input is invalid.

## How It Works

### 1. Data Loading
The program loads the historical dataset and calculates:
- Minimum and maximum fares across all classes
- Fare ranges for each cabin class (1st, 2nd, 3rd)
- All existing ticket numbers (to avoid duplicates)
- Survival statistics by class, gender, and age

### 2. Class Assignment
Based on your fare, you're assigned to a cabin class:
- **1st Class**: $5.00 - $512.33
- **2nd Class**: $9.69 - $73.50
- **3rd Class**: $3.17 - $69.55

**Note**: Zero-dollar fares (17 cases in historical data, likely crew or special circumstances) are excluded from range calculations to ensure accurate class boundaries.

**IMPORTANT - Overlapping Ranges**: Notice that the fare ranges overlap significantly:
- **$9.69 - $69.55**: Qualifies for ALL THREE classes → You get **1st Class** (highest priority)
- **$69.56 - $73.50**: Qualifies for 1st and 2nd classes → You get **1st Class**

**Examples**:
- Fare of $60: Could be 1st, 2nd, or 3rd → **Assigned to 1st Class**
- Fare of $70: Could be 1st or 2nd → **Assigned to 1st Class**  
- Fare of $10: Could be 1st, 2nd, or 3rd → **Assigned to 1st Class**
- Fare of $400: Only qualifies for 1st → **Assigned to 1st Class**

The system always assigns you to the **highest class** your fare qualifies for.

### 3. Ticket Number Generation
Generates a random 6-digit number that:
- Hasn't been used historically (not in the dataset)
- Hasn't been issued in this session
- Will keep regenerating until a unique number is found

### 4. Survival Calculation
Uses actual historical statistics:
- **By Class**: 1st (61.9%), 2nd (43.0%), 3rd (25.5%)
- **By Gender**: Female (72.7%), Male (19.1%)
- **By Age**: Children <16 (57.4%), Adults (39.2%), Elderly 60+ (30.0%)

The algorithm combines these factors to estimate your death probability.

### 5. Output
Creates a ticket file named `ticket_XXXXXX.txt` containing:
- Name
- Age
- Sex
- Fare
- Assigned Class
- Ticket Number

## Example Session

```
Loading historical Titanic data...
Loaded 1309 historical passenger records

============================================================
TITANIC TICKET BOOKING SYSTEM
============================================================

Fare Information:
Valid fare range: $3.17 - $512.33
1st Class: $5.00 - $512.33
2nd Class: $9.69 - $73.50
3rd Class: $3.17 - $69.55

Note: $0 fares excluded from range calculation

Found 596 historical 6-digit ticket numbers

Historical Survival Rates:
1st Class: 61.9%
2nd Class: 43.0%
3rd Class: 25.5%
Male: 19.1%
Female: 72.7%

============================================================
Welcome to Titanic Ticket Booking!
============================================================

Enter your name: John Smith

Enter your age: 35

Enter fare amount: $150

Enter your sex (male/female): male

Based on your fare of $150.00, you are assigned to Class 1

Your ticket number is: 847293

============================================================
Dear John Smith, your chances to die on our trip are 73.2%.
Enjoy your trip ☺
============================================================

Ticket saved to ticket_847293.txt

Thank you for booking with Titanic!
```

## Historical Dataset Details
- **Total passengers**: 1309
- **Survivors**: 500 (38.2%)
- **Deaths**: 809 (61.8%)
- **Classes**: 1st (323), 2nd (277), 3rd (708)
- **Gender**: Male (843), Female (466)
- **Age range**: 0.17 to 80 years old

## Notes
- The survival probability is calculated using real historical data
- Ticket numbers are guaranteed to be unique (not in historical data)
- The fare ranges have overlaps - higher class is always prioritized
- All inputs are validated with error messages and re-prompting

## Troubleshooting

### "Historical data file not found!"
**Problem**: The program cannot find titanic3.xls

**Solutions by environment**:
- **Local Python**: Make sure titanic3.xls is in the same folder as titanic_ticket_system.py
- **Google Colab**: Upload the file using the folder icon on the left sidebar
- **Jupyter Notebook**: Ensure the file is in the same directory as the .ipynb file
- **General**: When prompted, enter the full path to the file

### "Failed to read the data file!"
**Problem**: File found but cannot be read

**Solutions**:
1. Make sure the file is a valid Excel file (.xls format)
2. Install required libraries:
   ```bash
   pip install pandas openpyxl xlrd
   ```
3. Try re-downloading the titanic3.xls file if it may be corrupted

### "ModuleNotFoundError: No module named 'pandas'"
**Problem**: pandas library not installed

**Solutions by environment**:
- **Local Python**:
  ```bash
  pip install -r requirements.txt
  ```
  or
  ```bash
  pip install pandas openpyxl
  ```
- **Google Colab**: Run the first cell of the notebook (auto-installs)
- **Jupyter**: Install before starting Jupyter:
  ```bash
  pip install pandas openpyxl
  ```

### Google Colab Specific Issues

**Problem**: File upload button not visible
- **Solution**: Click the folder icon (📁) on the left sidebar

**Problem**: File disappears after runtime disconnects
- **Solution**: Re-upload the file each time you restart the runtime
- **Better solution**: Mount Google Drive and keep files there

**Problem**: Cells not running
- **Solution**: Check runtime status (top right). If disconnected, click "Connect"

### Jupyter Notebook Specific Issues

**Problem**: "Kernel not found" or "No kernel"
- **Solution**: 
  ```bash
  python -m ipykernel install --user
  ```

**Problem**: Notebook won't start
- **Solution**: 
  ```bash
  pip install --upgrade jupyter notebook
  ```

### General Python Issues

**Problem**: "python command not found"
- **Solution**: Try `python3` instead, or reinstall Python with "Add to PATH" checked

**Problem**: Permission denied on pip install
- **Solution**: Add `--user` flag:
  ```bash
  pip install --user pandas openpyxl
  ```

**Problem**: Multiple Python versions installed
- **Solution**: Use specific version:
  ```bash
  python3.8 -m pip install pandas openpyxl
  ```

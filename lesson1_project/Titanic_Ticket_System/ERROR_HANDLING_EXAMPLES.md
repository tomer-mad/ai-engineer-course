# Error Handling Example

## Scenario 1: File Not Found in Default Location

```
Loading historical Titanic data...

============================================================
ERROR: Historical data file not found!
============================================================

Could not find: 'titanic3.xls'

This file is REQUIRED to run the Titanic booking system.
The historical data is used to:
  • Validate fare ranges
  • Assign cabin classes
  • Prevent duplicate ticket numbers
  • Calculate survival probabilities

------------------------------------------------------------
Please choose an option:
  1. Enter a different file name or path
  2. Exit the program
------------------------------------------------------------

Your choice (1 or 2): 1

Enter the file name or full path to titanic3.xls: data/titanic3.xls

Attempting to load: data/titanic3.xls...
✓ Successfully loaded 1309 historical passenger records
  from: data/titanic3.xls
```

## Scenario 2: User Exits to Fix Location

```
Loading historical Titanic data...

============================================================
ERROR: Historical data file not found!
============================================================

Could not find: 'titanic3.xls'

This file is REQUIRED to run the Titanic booking system.
The historical data is used to:
  • Validate fare ranges
  • Assign cabin classes
  • Prevent duplicate ticket numbers
  • Calculate survival probabilities

------------------------------------------------------------
Please choose an option:
  1. Enter a different file name or path
  2. Exit the program
------------------------------------------------------------

Your choice (1 or 2): 2

Exiting program. Please place 'titanic3.xls' in the same
directory as this script and try again.
```

## Scenario 3: Invalid File Format

```
Loading historical Titanic data...

============================================================
ERROR: Failed to read the data file!
============================================================

File found but could not be read: 'titanic3.xls'
Error details: Excel file format cannot be determined, you must specify an engine manually.

Possible issues:
  • File may be corrupted
  • File may not be a valid Excel file
  • You may need to install openpyxl: pip install openpyxl

------------------------------------------------------------
Please choose an option:
  1. Try a different file
  2. Exit the program
------------------------------------------------------------

Your choice (1 or 2): 2

Exiting program.
```

# Quick Setup Guide - Titanic Ticket System

## For Absolute Beginners 🚀

### Easiest Method: Google Colab (5 minutes, no installation!)

#### Step 1: Go to Google Colab
1. Open your web browser
2. Go to: https://colab.research.google.com/
3. Sign in with your Google account (if not already signed in)

#### Step 2: Upload the Notebook
1. Click **"File"** in the top menu
2. Click **"Upload notebook"**
3. Click **"Choose File"**
4. Select **titanic_ticket_system.ipynb** from your downloads
5. Wait for it to upload

#### Step 3: Upload the Data File
1. Look at the **left sidebar**
2. Click the **folder icon** 📁
3. Click the **upload button** (looks like a file with an arrow)
4. Select **titanic3.xls** from your downloads
5. Wait for it to upload (you'll see it appear in the file list)

#### Step 4: Run the Program
1. Click **"Runtime"** in the top menu
2. Click **"Run all"**
3. Wait a few seconds for the cells to run
4. Scroll down to the last cell

#### Step 5: Book Your Ticket!
1. You'll see prompts asking for:
   - Your name
   - Your age
   - Fare amount ($3.17 - $512.33)
   - Your sex (male/female)
2. Type your answers and press Enter after each one
3. Get your ticket and survival probability! 🎫

---

## For Python Users: Local Installation

### Step 1: Check if Python is Installed
Open Command Prompt (Windows) or Terminal (Mac/Linux) and type:
```bash
python --version
```

If you see a version number (like "Python 3.10.5"), you're good!
If not, download from: https://www.python.org/downloads/

### Step 2: Install Required Libraries
In the same Command Prompt/Terminal, type:
```bash
pip install -r requirements.txt
```

If that doesn't work, try:
```bash
pip install pandas openpyxl
```

Or if you have Python 3:
```bash
pip3 install pandas openpyxl
```

### Step 3: Organize Your Files
Create a folder (for example, "TitanicProject") and put these files in it:
- titanic_ticket_system.py
- titanic3.xls

### Step 4: Run the Program
1. Open Command Prompt/Terminal
2. Navigate to your folder:
   ```bash
   cd path/to/TitanicProject
   ```
3. Run the program:
   ```bash
   python titanic_ticket_system.py
   ```
   
   Or:
   ```bash
   python3 titanic_ticket_system.py
   ```

### Step 5: Follow the Prompts
Answer the questions and get your ticket!

---

## Common Problems & Quick Fixes

### "python is not recognized" (Windows)
**Problem**: Python not in PATH
**Fix**: 
1. Reinstall Python from python.org
2. During installation, CHECK the box "Add Python to PATH"
3. Restart your computer

### "pip is not recognized"
**Problem**: pip not found
**Fix**: Try these in order:
```bash
python -m pip install pandas openpyxl
```
or
```bash
python3 -m pip install pandas openpyxl
```

### "No module named pandas"
**Problem**: Libraries not installed
**Fix**: 
```bash
pip install pandas openpyxl
```

### "File not found: titanic3.xls"
**Problem**: Data file not in the right place
**Fix**: 
- Make sure titanic3.xls is in the SAME folder as the .py file
- Or, when prompted, type the full path to the file

### Google Colab: "File disappeared"
**Problem**: Colab clears files when runtime restarts
**Fix**: 
- Re-upload titanic3.xls each time
- The upload button is in the left sidebar (folder icon)

---

## Video Tutorial Links

### For Google Colab:
- How to use Google Colab: https://www.youtube.com/results?search_query=google+colab+tutorial+for+beginners

### For Local Python:
- Installing Python (Windows): https://www.youtube.com/results?search_query=install+python+windows
- Installing Python (Mac): https://www.youtube.com/results?search_query=install+python+mac
- Using Command Prompt/Terminal: https://www.youtube.com/results?search_query=command+prompt+tutorial

---

## Still Having Issues?

### Check These:
1. ✓ Do you have an internet connection? (for Google Colab)
2. ✓ Is Python installed? Type `python --version` to check
3. ✓ Are both files (the .py or .ipynb AND titanic3.xls) in the same folder?
4. ✓ Did you install pandas and openpyxl?
5. ✓ Are you using the correct command (python vs python3)?

### Get Help:
- Read the full README.md for detailed instructions
- Check ERROR_HANDLING_EXAMPLES.md for common error messages
- Make sure you're using Python 3.x (not Python 2.x)

---

## What You'll Get

After running successfully, you'll receive:
1. **Your cabin class** (1st, 2nd, or 3rd) based on your fare
2. **A unique 6-digit ticket number**
3. **Your survival probability** based on historical data
4. **A ticket file** saved to your computer (ticket_XXXXXX.txt)

Enjoy your trip on the Titanic! ⚓🚢

# Python Lesson 02

## What I Learned Today

### 1. SQLAlchemy Database Operations

#### Creating a Database Model
```python
# Define a database table as a Python class
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)  # Note: expects date object, not string
    occupation = db.Column(db.String(80))
```

#### Database Initialization
```python
# This creates the database tables based on the model definitions
db.create_all()  # Safe to call multiple times - only creates missing tables
```

### 2. Saving Data to Database (Three-Step Process)

| Step | Code | What It Does |
|------|------|--------------|
| 1. Create object (in memory) | `form = Form(first_name="John", ...)` | Creates Python object, **not yet in database** |
| 2. Stage for insertion | `db.session.add(form)` | Adds object to session (staging area) |
| 3. Save to database | `db.session.commit()` | Actually writes to database |

**Important**: Without `db.session.commit()`, data is NOT saved to the database!

### 3. Converting String to Date Object

```python
from datetime import datetime  # Import datetime class, not just date

# Form data comes as string: "2025-12-09"
date_string = request.form["date"]

# Convert to date object for database
date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()

# Use date_obj because db.Column(db.Date) expects a date object, not a string
form = Form(date=date_obj)
```

### 4. HTML Radio Button Values

**Problem**: Radio buttons without `value` attribute send "on" as default value.

```html
<!-- Wrong: sends "on" to database -->
<input type="radio" name="occupation">

<!-- Correct: sends actual value -->
<input type="radio" name="occupation" value="Employed">
```

## What Was Difficult

Understanding the three-step database save process was confusing at first. I initially thought `Form()` or `db.session.add()` would save data, but only `db.session.commit()` actually writes to the database.

## Memo

This lesson covered Flask form handling with SQLAlchemy database integration, including proper data type conversion and HTML form attribute configuration. The key takeaway is understanding the staging nature of SQLAlchemy sessions where objects are prepared in memory before being committed to the database.

## Notes

### ○ Understanding `if __name__ == "__main__"`

#### What is `__name__`?

`__name__` is a special variable automatically set by Python:

| How the file is used | Value of `__name__` |
|---------------------|---------------------|
| Run directly: `python app.py` | `"__main__"` |
| Imported: `import app` | `"app"` (module name) |

#### Why use `if __name__ == "__main__"`?

```python
# Code here runs always (even when imported)

if __name__ == "__main__":
    # Code here runs ONLY when the file is executed directly
    app.run(debug=True, port=5001)
```

**Benefits**:
- Prevents code from running when the file is imported as a module
- Allows the file to be both executable and importable
- Useful for testing and code reusability

#### Dunder Variables (`__variable__`)

Variables with double underscores are called **"dunder" (double-underscore)** variables.

**Common dunder variables**:
- `__name__`: Module name or `"__main__"` when executed directly
- `__file__`: Path to the current file
- `__init__`: Constructor method in classes
- `__str__`: String representation of an object
- `__doc__`: Documentation string

These are **reserved by Python** for special purposes, not user-defined initial values.


### ○ VSCode Debugging (MacBook)

#### How to Open Debug View

1. **Open Debug Panel**
   - Shortcut: `Cmd + Shift + D`
   - Or click the bug icon on the left sidebar

2. **How to Start Debugging**
   - `Fn + F5`: Start debugging (see MacBook F-key note below)
   - `Fn + Ctrl + F5`: Run without debugging
   - Top menu: `Run > Start Debugging`

#### MacBook Function Keys (IMPORTANT!)

**Problem**: On MacBook, F5 key controls brightness/volume by default

**Solutions**:

1. **Use Fn key (Recommended)**
   - Press `Fn + F5` to start debugging
   - Press `Fn + F9` to toggle breakpoint
   - Press `Fn + F10` for step over
   - Press `Fn + F11` for step into

2. **Change System Settings (Optional)**
   - Go to: System Settings > Keyboard
   - Enable: "Use F1, F2, etc. keys as standard function keys"
   - After this change, F5 will work directly
   - Warning: You'll need Fn for volume/brightness instead

#### Keyboard Shortcuts

| Action | Shortcut | MacBook (with Fn) |
|--------|----------|-------------------|
| Open Debug View | `Cmd + Shift + D` | Same |
| Start Debugging | `F5` | `Fn + F5` |
| Run Without Debugging | `Ctrl + F5` | `Fn + Ctrl + F5` |
| Toggle Breakpoint | `F9` | `Fn + F9` |
| Step Over (next line) | `F10` | `Fn + F10` |
| Step Into (into function) | `F11` | `Fn + F11` |
| Step Out (out of function) | `Shift + F11` | `Fn + Shift + F11` |
| Continue | `F5` | `Fn + F5` |
| Stop Debugging | `Shift + F5` | `Fn + Shift + F5` |
| Restart | `Cmd + Shift + F5` | Same |

#### Types of Debugging

1. **Normal Debug (F5)**
   - Stops at breakpoints
   - Can inspect variables
   - Can step through code

2. **Run Without Debug (Ctrl + F5)**
   - Ignores breakpoints
   - Just runs the program
   - Faster execution

3. **Python-specific Debug Configurations**
   - Python File: Run current file
   - Module: Run as Python module
   - Remote Attach: Debug remote process
   - Django: Django application
   - Flask: Flask application

#### How to Use Debugger

1. **Setting Breakpoints**
   - Click on the left of line numbers (red dot appears)
   - Or place cursor on line and press `Fn + F9`
   - Click again to remove breakpoint

2. **Running Debug**
   - Press `Fn + F5`
   - First time: Select debug configuration from `.vscode/launch.json`
   - For Python: Choose "Python File"

3. **Inspecting Variables**
   - Check "Variables" section on left side of Debug view
   - Hover over variables in code to see values
   - Add variables to "Watch" for continuous monitoring

4. **Using Debug Console**
   - Find "Debug Console" tab at bottom
   - Can check variable values while running
   - Can execute code during debugging

#### How to Verify It's Working

1. **Check Breakpoint Stops**
   - Set a breakpoint and press `Fn + F5`
   - Execution should pause at breakpoint
   - Yellow arrow appears (current execution line)

2. **Check Debug Toolbar**
   - Appears at top when debugging starts
   - Has buttons for Continue, Step Over, Step Into, etc.
   - If you see this toolbar, debugging is active

3. **Check Variable Values**
   - "Variables" section on left shows values
   - Can see Local and Global variables
   - Values update as you step through code

4. **Check Call Stack**
   - "Call Stack" section on left side
   - Shows function call history
   - Can click to jump to different stack frames

#### Troubleshooting

- **Debug won't start**
  - Check if Python interpreter is correctly set
  - `Cmd + Shift + P` → "Python: Select Interpreter"
  - Make sure Python extension is installed

- **Breakpoint doesn't stop execution**
  - Make sure you're using Debug (`Fn + F5`), not Run (`Fn + Ctrl + F5`)
  - Check if the breakpoint line actually gets executed
  - Hollow red circle = breakpoint not bound (check file path)

- **F5 changes volume instead of debugging**
  - Use `Fn + F5` instead
  - Or change system keyboard settings (see MacBook F-key note above)


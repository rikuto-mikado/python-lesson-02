# Python Lesson 02 - Flask Form with Database & Email

A Flask web application that handles form submissions, stores data in SQLite database, and sends confirmation emails.

---

## Key Concepts Learned

### 1. SQLAlchemy Database Operations

#### Database Model Definition
```python
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)  # Expects date object, not string
    occupation = db.Column(db.String(80))
```

#### Three-Step Database Save Process

| Step | Code | Description |
|------|------|-------------|
| 1. **Create** | `form = Form(first_name="John", ...)` | Creates object in memory (NOT in database) |
| 2. **Stage** | `db.session.add(form)` | Adds object to session (staging area) |
| 3. **Commit** | `db.session.commit()` | Actually writes to database |

**Important**: Without `db.session.commit()`, data is NOT saved!

---

### 2. Date String Conversion

HTML form sends dates as strings → Database needs date objects

```python
from datetime import datetime

# Form data: "2025-12-09" (string)
date_string = request.form["date"]

# Convert to date object
date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()

# Use in database
form = Form(date=date_obj)
```

| Format Code | Meaning | Example |
|-------------|---------|---------|
| `%Y` | 4-digit year | 2025 |
| `%m` | 2-digit month | 12 |
| `%d` | 2-digit day | 09 |

---

### 3. HTML Form Handling

#### Radio Buttons - Value Attribute

```html
<!-- Wrong: Sends "on" to server -->
<input type="radio" name="occupation">

<!-- Correct: Sends actual value -->
<input type="radio" name="occupation" value="Employed">
```

#### Flash Messages (User Feedback)

```python
# Server-side (app.py)
flash(f"{first_name}, Your form was submitted successfully!", "success")
```

```html
<!-- Client-side (index.html) -->
{% with messages = get_flashed_messages() %}
    {% if messages %}
        <div class="alert alert-success">
            {% for message in messages %}
                {{ message }}
            {% endfor %}
        </div>
    {% endif %}
{% endwith %}
```

---

### 4. Email Sending with Flask-Mail

#### Email Message Structure

```python
# Create message body with f-strings
message_body = (
    f"Thank you for your submission, {first_name}.\n"
    f"Here are the details you provided: \n{first_name} {last_name}\n{date}\n"
    f"Thank you!!"
)

# Create Message object
message = Message(
    subject="New Form Submission",           # Email subject line
    sender=app.config["MAIL_USERNAME"],      # From address
    recipients=[email],                      # To address (list)
    body=message_body                        # Email content
)

# Send email via SMTP server
mail.send(message)
```

---

### 5. Environment Variables with `.env`

#### Why Use Environment Variables?

- Keep secrets out of code
- Easy configuration management
- Different settings for dev/prod
- Prevents accidental commits of sensitive data

#### Setup Process

**Step 1: Install python-dotenv**
```bash
pip install python-dotenv
```

**Step 2: Create `.env` file**
```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///data.db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx
MAIL_USERNAME=yourname@gmail.com
```

**Step 3: Load in `app.py`**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)

# Access environment variables
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))  # Convert to int
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "True"  # Convert to bool
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
```

#### Type Conversion Table

| Variable | .env Value | Python Type | Conversion |
|----------|------------|-------------|------------|
| MAIL_PORT | `"465"` | `int` | `int(os.getenv("MAIL_PORT"))` |
| MAIL_USE_SSL | `"True"` | `bool` | `os.getenv("MAIL_USE_SSL") == "True"` |
| SECRET_KEY | `"abc123"` | `str` | `os.getenv("SECRET_KEY")` |

**Important**: `os.getenv()` always returns strings. Convert to appropriate types!

**Step 4: Add to `.gitignore`**
```gitignore
.env
```

This prevents committing secrets to Git.

---

### 6. Gmail App Password Setup

For Gmail SMTP, you need an **App Password** (not your regular password):

1. Enable 2-Factor Authentication on Google Account
2. Go to: Google Account → Security → 2-Step Verification → App passwords
3. Generate app password for "Mail"
4. Copy the 16-character password (remove spaces)
5. Add to `.env` file:
```env
MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx
MAIL_USERNAME=yourname@gmail.com
```

---

## Technical Notes

### `if __name__ == "__main__"`

| How File is Used | `__name__` Value |
|-----------------|------------------|
| Run directly: `python app.py` | `"__main__"` |
| Imported: `import app` | `"app"` |

```python
if __name__ == "__main__":
    # This code runs ONLY when file is executed directly
    app.run(debug=True, port=5001)
```

### Database Initialization

```python
with app.app_context():
    db.create_all()  # Creates tables if they don't exist
```

- Safe to run multiple times
- Only creates missing tables
- Won't overwrite existing data

---

## Security Best Practices

1. Never commit `.env` file to Git
2. Use environment variables for secrets
3. Use Gmail App Passwords (not your real password)
4. Keep `.gitignore` updated
5. Use strong `SECRET_KEY` values

---

## What I Found Challenging

Understanding the three-step database process (`Form()` → `add()` → `commit()`) was initially confusing. Only `db.session.commit()` actually writes to the database.

---

## Summary

This lesson covered:
- Flask form handling with POST requests
- SQLAlchemy ORM for database operations
- Environment variable management with `.env`
- Sending emails with Flask-Mail and Gmail SMTP
- Flash messages for user feedback
- Data type conversions (string to date, string to int/bool)
- HTML form attributes (radio button values)

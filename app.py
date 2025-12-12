from datetime import datetime
import os
from dotenv import load_dotenv

# flash: Function to display one-time messages to users (e.g., success/error notifications after form submission)
from flask import Flask, render_template, request, flash

# Import SQLAlchemy for database functionality and initialize the database object
# This allows us to interact with databases using Python objects instead of raw SQL
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "True"
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")

db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    # Check if the form was submitted (POST request)
    # request.method contains the HTTP method used (GET or POST)
    if request.method == "POST":
        # Get data from the submitted form
        # request.form is a dictionary containing all form field values
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        occupation = request.form["occupation"]

        # Create a new Form instance
        form = Form(
            first_name=first_name,
            last_name=last_name,
            email=email,
            # Use date_obj (date object) instead of date (string) because the database column expects a Date type
            date=date_obj,
            occupation=occupation,
        )
        # Add the form object to the database session (staging for database insertion)
        # Note: This does NOT create duplicate entries - it only stages the object
        # The actual database insertion happens when db.session.commit() is called
        db.session.add(form)
        db.session.commit()

        # Create email message body using f-string formatting
        # \n creates line breaks in the email text
        message_body = (
            f"Thank you for your submission, {first_name}.\n"
            f"Here are the details you provided: \n{first_name} {last_name}\n{date}\n"
            f"Thank you!!"
        )
        # Create a Message object with email details
        # subject: Email subject line
        # sender: Email address sending the message (from .env MAIL_USERNAME)
        # recipients: List of email addresses to receive the message
        # body: The main text content of the email
        message = Message(
            subject="New Form Submission",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email],
            body=message_body,
        )
        # Send the email using Flask-Mail
        # This connects to the SMTP server (Gmail) and sends the message
        mail.send(message)

        flash(f"{first_name}, Your form was submitted successfully!", "success")

    # Render and return the HTML template
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        # Create all database tables based on the Form class definition (lines 13-19)
        # This creates a table with columns: id, first_name, last_name, email, date, occupation
        # Note: This does NOT create the form field variables - it creates the database structure
        # db.create_all() is safe to call multiple times - it only creates tables that don't exist yet
        # If data.db already exists with the tables, it won't duplicate or overwrite them
        db.create_all()
        app.run(debug=True, port=5001)

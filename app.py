from datetime import datetime

# flash: Function to display one-time messages to users (e.g., success/error notifications after form submission)
from flask import Flask, render_template, request, flash

# Import SQLAlchemy for database functionality and initialize the database object
# This allows us to interact with databases using Python objects instead of raw SQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "myapplicationsecretkey102030"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


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

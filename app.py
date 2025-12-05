from flask import Flask, render_template, request

app = Flask(__name__)


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
        occupation = request.form["occupation"]

    # Render and return the HTML template
    return render_template("index.html")


app.run(debug=True, port=5001)

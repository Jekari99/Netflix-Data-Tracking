import os
import pandas as pd
import requests
from flask import Flask, render_template, request, flash, session, redirect
from flask_session import Session
from secret_key_generator import secret_key_generator
from werkzeug.utils import secure_filename
from decouple import Config
from config import UPLOAD_FOLDER

app = Flask(__name__)

# Configures .env file and gets secret key
config = Config(".env")
secret_key = config.get("SECRET_KEY")


# Configure session to use filesystem
app.config["SESSION_TYPE"] = "filesystem"

# Set a secret key for the application
app.secret_key = secret_key

# Initialize the session extension
Session(app)

# Configures UPLOAD_FOLDER in config.py
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function that reads .csv file and does tasks
# Returns dataframe to be sent to renderNetflixData() function
def getNetflixData(fileName):
    df = pd.read_csv(fileName)
    df = df.drop(
        [
            "Profile Name",
            "Attributes",
            "Supplemental Video Type",
            "Device Type",
            "Bookmark",
            "Latest Bookmark",
            "Country",
        ],
        axis=1,
    )

    df["Start Time"] = pd.to_datetime(df["Start Time"], utc=True)
    df = df.set_index("Start Time")
    df.index = df.index.tz_convert("US/Eastern")
    df = df.reset_index()
    df["Duration"] = pd.to_timedelta(df["Duration"])
    return df


# Function to render the dataframe in the html table
# Works for sample file and uploaded file
def renderNetflixData(filename):
    if filename == "SampleNetflixViewingHistory.csv":
        file_path = os.path.join("files", filename)
        df = getNetflixData(file_path)
        return render_template(
            "data.html",
            tables=[df.to_html(classes="data-table")],
            titles=[""],
        )
    else:
        df = getNetflixData(filename)
        return render_template(
            "data.html",
            tables=[df.to_html(classes="data-table")],
            titles=[""],
        )


# Renders index.html
@app.route("/")
def index():
    return render_template("index.html")


# Renders data.html
@app.route("/data")
def data():
    return render_template("data.html")


# Renders about.html
@app.route("/about")
def about():
    return render_template("about.html")


# Route to handle form submission for the sample form button
@app.route("/sample", methods=["POST"])
def uploadSample():
    if request.method == "POST":
        session.clear()
        return renderNetflixData("SampleNetflixViewingHistory.csv")


# Route to handle form submission for the upload file form button
# Gets uploaded file name using requests
# Saves file by securing it and storing it in the proper directory, files
# Adds uploaded file to the session in the app
@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        uploaded_file = request.files["filename"]
        if uploaded_file.filename != "":
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            session["uploaded_file"] = filename
            return renderNetflixData(
                os.path.join(app.config["UPLOAD_FOLDER"], filename)
            )


# Route to handle the search form submission
# Gets the search query from the form using reqeust
# Checks if the uploaded file is in session, if so, search using that file
# Else, use the sample file
# Calls a function that filters the file based on the query
@app.route("/search", methods=["POST"])
def searchNetflixData():
    if request.method == "POST":
        search_query = request.form.get("search_query")
        if search_query != "":
            if "uploaded_file" in session:
                uploaded_filename = session["uploaded_file"]
                return filterNetflixData(search_query, uploaded_filename)
            else:
                return filterNetflixData(
                    search_query, "SampleNetflixViewingHistory.csv"
                )


# Function that takes in the search query and filters the dataframe based on that query
def filterNetflixData(search_query, filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    # Load the data from the specified file
    df = pd.read_csv(file_path)

    # Perform necessary data transformations and rendering
    df = df.drop(
        [
            "Profile Name",
            "Attributes",
            "Supplemental Video Type",
            "Device Type",
            "Bookmark",
            "Latest Bookmark",
            "Country",
        ],
        axis=1,
    )
    df["Start Time"] = pd.to_datetime(df["Start Time"], utc=True)
    df = df.set_index("Start Time")
    df.index = df.index.tz_convert("US/Eastern")
    df = df.reset_index()
    df["Duration"] = pd.to_timedelta(df["Duration"])

    # Filter the DataFrame based on the search_query
    filtered_df = df[df["Title"].str.contains(search_query, regex=False)]
    if filtered_df.empty:
        flash("No matching entries found.")
        return redirect("/sample")

    return render_template(
        "data.html",
        tables=[filtered_df.to_html(classes="data-table")],
        titles=[""],
    )


# App debugging
if __name__ == "__main__":
    app.run(debug=True)

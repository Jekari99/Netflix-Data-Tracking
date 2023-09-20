import os
import pandas as pd
import requests
from flask import Flask, render_template, request, flash, session, redirect
from flask_session import Session
from secret_key_generator import secret_key_generator
from werkzeug.utils import secure_filename
from decouple import Config


app = Flask(__name__)
script_directory = os.path.dirname(os.path.abspath(__file__))
print(script_directory)

config = Config(".env")
secret_key = config.get("SECRET_KEY")


# Configure session to use filesystem (you can change this to use other storage options)
app.config["SESSION_TYPE"] = "filesystem"

# Set a secret key for your application (replace 'your_secret_key' with a secure key)
# SECRET_KEY = secret_key_generator.generate()
app.secret_key = secret_key

# Initialize the session extension
Session(app)


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


def renderNetflixData(filename):
    df = getNetflixData(filename)
    return render_template(
        "data.html",
        tables=[df.to_html(classes="data-table")],
        titles=[""],
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    return render_template("data.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/sample", methods=["POST"])
def uploadSample():
    if request.method == "POST":
        return renderNetflixData("SampleNetflixViewingHistory.csv")


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        uploaded_file = request.files["filename"]
        if uploaded_file.filename != "":
            # file_path = os.path.join(script_directory, uploaded_file.filename)
            # uploaded_file.save(file_path)
            # result = process_file(file_path)
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(script_directory, filename))
            return renderNetflixData(os.path.join(script_directory, filename))
        else:
            flash("Please select a file to upload.")
            return redirect("/sample")
        # return renderNetflixData(uploaded_file.filename)


def process_file(file_path):
    # Implement your file processing logic here
    # You can read the file and generate content as needed
    with open(file_path, "r") as file:
        file_content = file.read()
    return file_content


@app.route("/search", methods=["POST"])
def searchNetflixData():
    if request.method == "POST":
        search_query = request.form.get("search_query")
        if search_query != "":
            if "uploaded_file" in session:
                uploaded_filename = session["uploaded_file"]
                print("this is the file name")
                print(uploaded_filename)
                return filterNetflixData(search_query, uploaded_filename)
            else:
                return filterNetflixData(
                    search_query, "SampleNetflixViewingHistory.csv"
                )
        else:
            flash("Please enter a search query.")
            return redirect("/sample")


def filterNetflixData(search_query, filename):
    # Load the data from the specified file
    df = pd.read_csv(filename)
    search = search_query

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
    filtered_df = df[df["Title"].str.contains(search, regex=False)]
    if filtered_df.empty:
        flash("No matching entries found.")
        return redirect("/sample")

    return render_template(
        "data.html",
        tables=[filtered_df.to_html(classes="data-table")],
        titles=[""],
    )


if __name__ == "__main__":
    app.run(debug=True)

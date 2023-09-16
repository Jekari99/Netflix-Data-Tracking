import os
import pandas as pd
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
script_directory = os.path.dirname(os.path.abspath(__file__))


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

    return render_template("data.html", tables=[df.to_html()], titles=[""])


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
        return getNetflixData("SampleNetflixViewingHistory.csv")


@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["filename"]
    if uploaded_file.filename != "":
        file_path = os.path.join(script_directory, uploaded_file.filename)
        uploaded_file.save(file_path)
        # Process the uploaded file here
        result = process_file(file_path)
    return getNetflixData(uploaded_file.filename)


def process_file(file_path):
    # Implement your file processing logic here
    # You can read the file and generate content as needed
    with open(file_path, "r") as file:
        file_content = file.read()
    return file_content


if __name__ == "__main__":
    app.run(debug=True)

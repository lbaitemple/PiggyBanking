from flask import Flask, render_template, send_from_directory, request
from dotenv import load_dotenv
import csv
import requests
import os
import json

load_dotenv()

app = Flask(__name__, static_url_path="/static")

with open("processed_senators.json", "r") as infile:
    data = json.load(infile)
    

@app.route("/")
def home():
    return render_template("pages/dailysummary.html", data=data)


@app.route("/official")
def dashboard():
    official = request.args.get("official")
    return render_template("pages/dashboard.html", official=official, data=data)

@app.route("/about")
def about():
    return render_template("pages/about.html")

@app.route("/overview")
def overview():
    return render_template("pages/overview.html")

@app.route("/lesson1.html")
def lesson1():
    return render_template("pages/lesson1.html") 

@app.route("/lesson2.html")
def lesson2():
    return render_template("pages/lesson2.html") 

@app.route("/lesson3.html")
def lesson3():
    return render_template("pages/lesson3.html") 

@app.route("/lesson4.html")
def lesson4():
    return render_template("pages/lesson4.html") 


#if __name__ == "__main__":
#    app.run(debug=True)

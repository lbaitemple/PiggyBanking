from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from dotenv import load_dotenv
import csv
import requests
import os
import json
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

with open("processed_senators.json", "r") as infile:
    data = json.load(infile)
load_dotenv()

with open("processed_senators.json", "r") as infile:
    data = json.load(infile)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("pages/dailysummary.html", data=data)
    else:
        return redirect(url_for('login'))

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('about'))
        else:
            return 'Login Failed'

    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
@app.route("/register/", methods=["GET", "POST"])
def register():
    print("Register route called")  # Add this line for debugging

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already taken'
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
 
    app.run(host='0.0.0.0', debug=True)

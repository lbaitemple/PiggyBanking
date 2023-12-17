from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import boto3

app = Flask(__name__, static_url_path="/static")
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('zany-pink-abalone-gearCyclicDB')





class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

    @classmethod
    def get(cls, user_id):
        try:
            response = table.get_item(Key={'id': user_id})
            user_item = response.get('Item')
            if user_item:
                return User(user_item['id'], user_item['username'], user_item['password'])
            return None
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None

        

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/logout")
@login_required
def logout():
    return redirect(url_for('home'))
    logout_user()

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
    app.run(host='0.0.0.0', debug=True)

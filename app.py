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

@login_manager.user_loader
def load_user(user_id):
    response = table.get_item(Key={'id': user_id})
    user_item = response.get('Item')
    if user_item:
        return User(user_item['id'], user_item['username'], user_item['password'])
    return None

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

# Other routes...

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

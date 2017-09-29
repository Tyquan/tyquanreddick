from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import Request, urlopen
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user

from mockdbhelper import MockDBHelper as DBHelper
from user import User

app = Flask(__name__)
login_manager = LoginManager(app)

app.secret_key = 'pPXJA3C37Qybz4QykP+hOyUvVQeEXk1Ao4C8upz+fGQXKsM'

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

#Log user in route
@app.route("/login", methods=["POST"])
def login():
	email = request.form.get("email")
	password = request.form.get("password")
	user_password = DB.get_user(email)
	if user_password and user_password == password:
		user = User(email)
		login_user(user)
		return redirect(url_for('account'))

#load user
@login_manager.user_loader
def load_user(user_id):
	user_password = DB.get_user(user_id)
	if user_password:
		return User(user_id)

## Accont cant go here unless logged in
@app.route("/account")
@login_required
def account():
	return "You are logged in"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import Request, urlopen

from flask_login import logout_user
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user

from passwordhelper import PasswordHelper
from mockdbhelper import MockDBHelper as DBHelper
from user import User

PH = PasswordHelper()
DB = DBHelper()

app = Flask(__name__)
login_manager = LoginManager(app)

app.secret_key = 'pPXJA3C37Qybz4QykP+hOyUvVQeEXk1Ao4C8upz+fGQXKsM'

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# sign a user up
@app.route("/register", methods=["POST"])
def register():
	email = request.form.get("email")
	pw1 = request.form.get("password")
	pw2 = request.form.get("password2")
	if not pw1 == pw2:
		return redirect(url_for('index'))
	if DB.get_user(email):
		return redirect(url_for('index'))
	salt = PH.get_salt()
	hashed = PH.get_hash(pw1 + salt)
	DB.add_user(email, salt, hashed)
	return redirect(url_for('index'))

#Log user in route
@app.route("/login", methods=["POST"])
def login():
	email = request.form.get("email")
	password = request.form.get("password")
	stored_user = DB.get_user(email)
	if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
		user = User(email)
		login_user(user, remember=True)
		return redirect(url_for('account'))
	return index()

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

## Log a user out
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
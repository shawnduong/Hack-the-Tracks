import os
import sys

from flask import *
from flask_sqlalchemy import *
from flask_login import LoginManager, current_user, login_user, logout_user

from wordlists.users import USERS

# Instantiate the application and define settings.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.urandom(24)

# Load the database.
db = SQLAlchemy(app)
from models import *
with app.app_context():
	db.create_all()

# All of the target accounts are created upon start just in case participants
# accidentally nuke the database while learning SQLi.
db.session.execute("DELETE FROM user;")
for user in USERS.keys():
	User.register(user, USERS[user])

# Authentication.
from authentication import *

# Website routes.
from routes import *

# API endpoints, used by HackerPass units.
from api import *

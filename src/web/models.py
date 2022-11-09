from __future__ import annotations

import bcrypt

from app import db

from flask_login import UserMixin
from typing import Union

class User(UserMixin, db.Model):
	"""
	A definition for a single user, consisting of a username and password.
	"""

	__tablename__ = "user"

	id       = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(256), unique=True , nullable=False)
	password = db.Column(db.String(256), unique=False, nullable=False)

	def __init__(self, username="", password="", acctType=""):
		"""
		Constructor method for User type objects.
		"""

		self.username = username
		self.password = password

	def login(username: str, password: str) -> Union[User, bool]:
		"""
		Check if the username and password are valid, returning a User object
		if successful, or False if unsuccessful.
		"""

		if ((user:=User.query.filter_by(username=username).first()) != None
			and bcrypt.checkpw(password.encode(), user.password)
		):
			return user
		else:
			return False


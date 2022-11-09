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

		userid = None

		# Username input field is deliberately vulnerable to an SQLi. Never
		# use this code in real life or else you'll be vulnerable to an SQLi!
		sql = f"SELECT * FROM user WHERE username='{username}' AND password='{password}';"
		result = db.session.execute(sql).all()

		if len(result) > 0:
			userid = result[0][0]
		print(userid)

		db.session.commit()

		# The above code was just to be vulnerable. We still need to return
		# a User object.
		if userid != None:
			print("true")
			return User.query.get(userid)

		return False

	def register(username: str, password: str) -> bool:
		"""
		Attempt to register a user, returning True if successful or False if
		the registration failed.
		"""

		try:
			if User.query.filter_by(username=username).first() == None:
				# Passwords are deliberately unencrypted. Don't do this IRL!
				sql = f"INSERT INTO user(username,password) VALUES ('{username}','{password}');"
				result = db.session.execute(sql)
				db.session.commit()
				return True
		except:
			return False

		return False


from app import *

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

# Define user login functionality.
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

@loginManager.user_loader
def load_user(id: int):
	"""
	Load a user using their id.
	"""

	return User.query.get(id)

@app.route("/login", methods=["POST"])
def login():
	"""
	Authenticate the user.
	"""

	user = User.login(request.form["username"], request.form["password"])

	# Failed login condition.
	if user == False:
		return render_template("index.html", failed=True)

	login_user(user)
	return redirect(url_for("application"))

@app.route("/logout", methods=["GET"])
@login_required
def logout():
	"""
	Log a user out of the application and take them to the index.
	"""

	logout_user()
	return render_template("index.html")


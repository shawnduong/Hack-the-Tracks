from app import *

import subprocess

@app.route("/grep", methods=["POST"])
@login_required
def vuln_grep():
	"""
	Vulnerable API endpoint literally executes whatever commands you POST to it
	and then returns the output.
	"""

	command = "grep " + request.json["command"] + " data/logs.txt"

	try:
		output = {"result": subprocess.check_output(command, shell=True).decode("utf-8")}
	except subprocess.CalledProcessError as err:
		output = {"result": f"Command: {command} failed."}

	return output

@app.route("/sql", methods=["POST"])
@login_required
def vuln_sql():
	"""
	Vulnerable API endpoint may leak a database.
	"""

	sql = f"SELECT * FROM logs WHERE date=\"{request.json['command']}\";"

	try:
		result = db.session.execute(sql).all()
		output = {"result": "\n".join([str(r) for r in result])}
	except Exception as err:
		output = {"result": f"Query failed: {err}"}

	return output


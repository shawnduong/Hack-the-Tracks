from app import *

import subprocess

@app.route("/api", methods=["POST"])
def vuln():
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


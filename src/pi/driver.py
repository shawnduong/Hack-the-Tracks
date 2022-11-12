#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os
import time

# Make sure that the railmaster group has the right permissions for this directory.
DIR = "/tmp/rail/"
F_V = DIR + "velocity.txt"
F_T = DIR + "turnout.txt"

def main():

	# 11,13,33 = A (tracks); 16,18 = B (turnout)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(11, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)
	GPIO.setup(33, GPIO.OUT)
	GPIO.setup(16, GPIO.OUT)
	GPIO.setup(18, GPIO.OUT)

	GPIO.output(11, GPIO.HIGH)
	GPIO.output(13, GPIO.LOW)

	# ENA PWM pin 33 with frequency 0.5.
	ena = GPIO.PWM(33, 100)
	ena.start(0)

	# Status variables.
	velocity = 0
	reverse  = False
	crossed  = False

	# Forced initialization prevents rapid start.
	if not os.path.exists(DIR):
		os.makedirs(DIR)
	open(F_V, "w").write("0")
	open(F_T, "w").write("y")
	os.chmod(F_V, 0o777)
	os.chmod(F_T, 0o777)

	# Main loop.
	try:
		while True:

			# Read the velocity.
			v = int(open(F_V, "r").read())

			if v != velocity:

				# Reverse.
				if v < 0:

					# Flip the voltage if needed.
					if reverse != True:
						print("Direction change to reverse.")
						GPIO.output(11, GPIO.LOW)
						GPIO.output(13, GPIO.HIGH)
						reverse = True

					# Duty cycle is strictly positive. Voltage determined direction.
					print(f"{v=}")
					ena.ChangeDutyCycle(-v)
					velocity = v

				else:

					# Flip the voltage if needed.
					if reverse == True:
						print("Direction change to forward.")
						GPIO.output(11, GPIO.HIGH)
						GPIO.output(13, GPIO.LOW)
						reverse = False

					print(f"{v=}")
					ena.ChangeDutyCycle(v)
					velocity = v

			# Read the turnout.
			t = open(F_T, "r").read()

			if t == "y" and crossed == True:
				print("Turnout through position.")
				GPIO.output(16, GPIO.HIGH)
				GPIO.output(18, GPIO.LOW)
				time.sleep(0.2)
				GPIO.output(16, GPIO.LOW)
				GPIO.output(18, GPIO.LOW)
				crossed = False
			elif t == "x" and crossed == False:
				print("Turnout crossed position.")
				GPIO.output(16, GPIO.LOW)
				GPIO.output(18, GPIO.HIGH)
				time.sleep(0.2)
				GPIO.output(16, GPIO.LOW)
				GPIO.output(18, GPIO.LOW)
				crossed = True

			# Limit updates to 1 per second.
			time.sleep(1)
	except KeyboardInterrupt:
		print("Quitting.")

	GPIO.cleanup()

if __name__ == "__main__":
	main()

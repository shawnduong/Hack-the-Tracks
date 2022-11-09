#!/usr/bin/env python3
# Generate database.sqlite and logs.txt containing railroad logs.

import sqlite3
from datetime import date, datetime, time, timedelta
from random import randint

START  = date(2022,  1,  1)
END    = date(2022, 11, 12)

ARRIVALS = {
	timedelta(hours=7, minutes=30): {
		"TN-102": "SAC",
		"TS-100": "MOD",
		"TS-109": "MER",
	},
	timedelta(hours=9): {
		"TN-102": "MOD",
		"TS-100": "MER",
		"TS-109": "MOD",
	},
	timedelta(hours=10, minutes=30): {
		"TN-102": "MER",
		"TS-100": "MOD",
		"TS-109": "SAC",
	},
	timedelta(hours=12): {
		"TN-102": "MOD",
		"TS-100": "SAC",
		"TS-109": "MOD",
	},
	timedelta(hours=13, minutes=30): {
		"TN-102": "SAC",
		"TS-100": "MOD",
		"TS-109": "MER",
	},
	timedelta(hours=15): {
		"TN-102": "MOD",
		"TS-100": "MER",
		"TS-109": "MOD",
	},
	timedelta(hours=16, minutes=30): {
		"TN-102": "MER",
		"TS-100": "MOD",
		"TS-109": "SAC",
	},
	timedelta(hours=18): {
		"TN-102": "MOD",
		"TS-100": "SAC",
		"TS-109": "MOD",
	},
	timedelta(hours=19, minutes=30): {
		"TN-102": "SAC",
		"TS-100": "MOD",
		"TS-109": "MER",
	},
}

def main():

	output = []

	for i in range((END-START).days + 1):

		for d in ARRIVALS.keys():

			for t in ARRIVALS[d].keys():

				a = str(START + timedelta(days=i))
				b = str(d + timedelta(minutes=randint(0,30), seconds=randint(0,60)))

				if len(b) != len("00:00:00"):
					b = "0" + b

				output.append(f"{a} {b} Train {t} arrived at {ARRIVALS[d][t]}.\n")

	output.sort()

	open("logs.txt", "w").write("".join(output))
	print("Created logs.txt.")

	values = []
	con = sqlite3.connect("logs.sqlite")
	cur = con.cursor()
	cur.execute("CREATE TABLE logs(date, time, event);")

	for line in output:
		tokens = line.strip("\n").split()
		a = tokens[0]
		b = tokens[1]
		c = " ".join(tokens[2::])

		cur.execute(f"INSERT INTO logs VALUES ('{a}','{b}','{c}')")

	con.commit()
	print("Created logs.sqlite.")

if __name__ == "__main__":
	main()

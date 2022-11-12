#!/usr/bin/env python3

import curses
import time

# Make sure that the railmaster group has the right permissions for this directory.
DIR = "/tmp/rail/"
F_V = DIR + "velocity.txt"
F_T = DIR + "turnout.txt"

def main():

	# Set up TUI.
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	stdscr.keypad(True)
	stdscr.clear()

	# Non-blocking getch.
	stdscr.nodelay(True)

	start = 2

	stdscr.addstr(start+ 1, 1, f" ======[ Railway Systems Control Panel ]====  ")
	stdscr.addstr(start+ 3, 1, f"  There are currently (1) active train(s).    ")
	stdscr.addstr(start+ 4, 1, f"  Selected train: [ Amtrak California 80211 ] ")
	stdscr.addstr(start+ 6, 1, f"     Increase train velocity.                 ")
	stdscr.addstr(start+ 7, 1, f"     Decrease train velocity.                 ")
	stdscr.addstr(start+ 8, 1, f"  x  Turnout cross orientation.               ")
	stdscr.addstr(start+ 9, 1, f"  y  Turnout through orientation.             ")
	stdscr.addstr(start+10, 1, f"  q  Quit the control panel.                  ")
	stdscr.addch(start+6, 3, curses.ACS_RARROW, curses.A_ALTCHARSET)
	stdscr.addch(start+7, 3, curses.ACS_LARROW, curses.A_ALTCHARSET)

	# Main loop.
	while True:

		try:
			v = int(open(F_V, "r").read())
		except:
			open(F_V, "w").write("0")
			v = 0

		# Update the screen.
		stdscr.addstr(start+12, 1, f"  Current velocity = {v} mph.   ")

		c = stdscr.getch()

		if c == ord("q"):
			break
		elif c == curses.KEY_RIGHT and v + 1 <= 100:
			open(F_V, "w").write(str(v+1))
		elif c == curses.KEY_LEFT and v - 1 >= -100:
			open(F_V, "w").write(str(v-1))
		elif c == ord("x"):
			open(F_T, "w").write("x")
		elif c == ord("y"):
			open(F_T, "w").write("y")

		time.sleep(0.1)

	# End the TUI.
	curses.echo()
	curses.nocbreak()
	curses.curs_set(1)
	stdscr.keypad(False)
	curses.endwin()

if __name__ == "__main__":
	main()

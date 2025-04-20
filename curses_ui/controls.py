"""
These are various user input checks i want to recycle.
"""


def scroll_instructions(stdscr, line):
    stdscr.addstr(line, 0, "↑↓ or jk to move | Enter to edit/run | q to quit")


def scroll(key):
    if key in (curses.KEY_UP, ord("k")):
        selected = (selected - 1) % 3
    elif key in (curses.KEY_DOWN, ord("j")):
        selected = (selected + 1) % 3
    pass


def check_exits(key):
    """
    Checks if user inputted 'q' or 'esc'.

    Returns False on 'esc'. Exits program on 'q'.
    """
    if key == 27:
        return False
    if key == ord("q") or key == ord("Q"):
        exit(0)
    return True


def write():
    pass

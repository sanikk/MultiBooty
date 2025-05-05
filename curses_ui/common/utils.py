"""
Mostly just sketches for recycleable UI components.
This one is unsorted first drafts.
"""


def handle_return_value(stdscr, ret):
    if ret.success:
        stdscr.addstr("Done! No errors.")
        return True
    for error in ret.errors:
        stdscr.addstr(error)
    return False


def print_lines(stdscr, lines):
    for line in lines:
        stdscr.addstr(line + "\n")

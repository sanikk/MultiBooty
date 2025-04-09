import curses
import sys
from typing import Callable

# import curses_ui.controls

# from curses_ui import controls


def text_prompt(stdscr, line, col):
    curses.echo()
    stdscr.move(line, col)
    stdscr.clrtoeol()
    stdscr.refresh()
    input_str = stdscr.getstr().decode("utf-8")
    curses.noecho()
    if input_str:
        return input_str


def numeric_prompt(stdscr, offset, default):
    text_str = f"{default}"
    while True:
        key = stdscr.getch()

        if key == 27:
            return ""
        elif key in (10, curses.KEY_ENTER):
            stdscr.noecho()
            return text_str
        elif key in range(48, 58):  # Number keys 0-9
            text_str += chr(key)
            stdscr.addch(chr(key))

        elif key in (127, curses.KEY_BACKSPACE, 8) and text_str:
            text_str = text_str[:-1]
            y, x = stdscr.getyx()
            if x > 0:
                stdscr.move(y, x - 1)
                stdscr.delch()
        elif not numeric:
            text_str += chr(key)


def selection_box(
    stdscr,
    message: str,
    choices: list[str],
    callback: Callable[[str], None],
    default_index: int = 0,
):

    selected = default_index
    max_y, max_x = stdscr.getmaxyx()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, message, curses.A_BOLD)
        for idx, choice in enumerate(choices):
            attr = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            stdscr.addstr(2 + idx, 2, choice, attr)
        stdscr.addstr(
            max_y - 1,
            0,
            "↑↓ or jk to move | Enter to select | Esc to cancel | q to quit",
        )
        stdscr.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % len(choices)
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % len(choices)
        elif key in (10, 13):
            callback(choices[selected])
            return
        elif key == 27:  # ESC
            return
        elif key == ord("q"):
            curses.endwin()
            exit(0)

from typing import Callable
from curses import KEY_ENTER, endwin, window, echo, noecho, KEY_BACKSPACE, newwin

from curses_ui.common.controls import change_selection, check_quit_esc
from curses_ui.common.prints import print_menu


def text_prompt(stdscr, line, col):
    echo()
    stdscr.move(line, col)
    stdscr.clrtoeol()
    stdscr.refresh()
    input_str = stdscr.getstr().decode("utf-8")
    noecho()
    if input_str:
        return input_str


def numeric_prompt(stdscr, offset, default):
    text_str = f"{default}"
    while True:
        key = stdscr.getch()

        if key == 27:
            return ""
        elif key in (10, KEY_ENTER):
            stdscr.noecho()
            return text_str
        elif key in range(48, 58):  # Number keys 0-9
            text_str += chr(key)
            stdscr.addch(chr(key))

        elif key in (127, KEY_BACKSPACE, 8) and text_str:
            text_str = text_str[:-1]
            y, x = stdscr.getyx()
            if x > 0:
                stdscr.move(y, x - 1)
                stdscr.delch()


def selection_box(
    stdscr: window,
    message: str | list[str],
    choices: list[str],
    callback: Callable,
    default_index: int = 0,
):

    selected = default_index
    center_y, center_x = [a // 2 for a in stdscr.getmaxyx()]

    msg_height = len(message) if isinstance(message, list) else 1
    height = msg_height + len(choices) + 4
    # height = (len(message) if isinstance(message, list) else 1) + len(choices) + 2
    width = (
        # just get the longest line length and pad that with 2
        max(map(len, choices + (message if isinstance(message, list) else [message])))
        + 4
    )
    start_y = center_y - height // 2
    start_x = center_x - width // 2

    box_win = newwin(height, width, start_y, start_x)
    box_win.box()

    def close_window(box_win: window):
        del box_win
        stdscr.touchwin()
        stdscr.refresh()

    while True:
        linenumber = 1
        if isinstance(message, str):
            box_win.addstr(linenumber, 2, message)
        elif isinstance(message, list):
            for message_line in message:
                box_win.addstr(linenumber, 2, message_line)
                linenumber += 1

        print_menu(
            stdscr=box_win,
            menu_items=choices,
            selected=selected,
            start_y=linenumber + 1,
        )

        key = box_win.getch()
        if check_quit_esc(key=key):
            close_window(box_win)
            return
        selected = change_selection(key=key, selected=selected, menu_items=choices)
        if key in (10, KEY_ENTER):
            endwin()
            print(choices[selected])
            callback(selected)
            close_window(box_win)
            return
        elif ord("0") < key < ord(str(len(choices) + 1)):
            endwin()
            print(choices[key - ord("1")])
            callback(key - ord("1"))
            close_window(box_win)
            return

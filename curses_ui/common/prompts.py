from typing import Callable
from curses import KEY_ENTER, window, echo, noecho, newwin, KEY_BACKSPACE

from curses_ui.common.controls import change_selection, check_quit_esc, close_window
from curses_ui.common.prints import print_menu
from curses_ui.common.windows import popup_window


def text_prompt(win: window, line: int, col: int):
    echo()
    win.move(line, col)
    win.clrtoeol()
    win.refresh()
    input_str = win.getstr().decode("utf-8")
    noecho()
    if input_str:
        return input_str


def text_prompt_box(
    stdscr: window,
    height: int,
    width: int,
    message: list[str],
    getter: Callable,
    setter: Callable,
):
    win = popup_window(stdscr=stdscr, height=height, width=width)
    while True:
        linenumber = 1
        for linetext in message:
            win.addstr(linenumber, 1, linetext)
            linenumber += 1
        linenumber += 1
        win.addstr(linenumber, 1, f"Previous value: {getter()}")
        linenumber += 2
        win.refresh()

        win.move(linenumber, 2)
        input_str = ""
        while True:
            ch = win.getch()
            if ch in (10, 13):
                if setter(input_str):
                    close_window(stdscr=stdscr, win=win)
                    return
            elif ch == 27:
                return
            elif ch in (8, 127, KEY_BACKSPACE):
                if input_str:
                    input_str = input_str[:-1]
                    y, x = win.getyx()
                    win.move(y, x - 1)
                    win.delch()
            elif 32 <= ch < 127:  # Printable ASCII
                input_str += chr(ch)
                win.addch(ch)


def selection_box(
    stdscr: window,
    message: list[str],
    choices: list[str | bool],
    callback: Callable,
    default_index: int = 0,
):

    selected = default_index
    center_y, center_x = [a // 2 for a in stdscr.getmaxyx()]

    msg_height = len(message) if isinstance(message, list) else 1
    height = msg_height + len(choices) + 4
    # just get the longest line length and pad that with 2
    width = max(map(lambda x: len(str(x)), choices + message)) + 4
    start_y = center_y - height // 2
    start_x = center_x - width // 2

    box_win = newwin(height, width, start_y, start_x)
    box_win.box()

    while True:
        linenumber = 1
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
            close_window(stdscr=stdscr, win=box_win)
            return
        selected = change_selection(key=key, selected=selected, menu_items=choices)
        if key in (10, KEY_ENTER):
            callback(selected)
            close_window(stdscr=stdscr, win=box_win)
            return
        elif ord("0") < key < ord(str(len(choices) + 1)):
            callback(key - ord("1"))
            close_window(stdscr=stdscr, win=box_win)
            return

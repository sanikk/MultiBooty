from curses import window, endwin
from typing import Callable


def curses_runner(fn: Callable, stdscr: window, *args, **kwargs):
    """
    Closes curses and restarts it.
    Using this prevents bleed over from sudo runners
    """
    endwin()
    try:
        ret = fn(*args, **kwargs)
    finally:
        stdscr.refresh()
    return ret

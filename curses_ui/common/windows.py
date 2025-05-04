from curses import window, newwin


def popup_window(stdscr: window, height: int, width: int):

    center_y, center_x = [a // 2 for a in stdscr.getmaxyx()]

    # just get the longest line length and pad that with 2
    start_y = center_y - height // 2
    start_x = center_x - width // 2

    win = newwin(height, width, start_y, start_x)
    win.box()
    return win


def close_window(stdscr: window, win: window):
    del win
    stdscr.touchwin()
    stdscr.refresh()

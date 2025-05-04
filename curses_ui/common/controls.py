from curses import KEY_UP, KEY_DOWN, window


def check_quit_esc(key: int):
    if key == 27:
        return True
    if key == ord("q") or key == ord("Q"):
        exit(0)
    return False


def change_selection(key: int, selected: int, menu_items: list):
    if key in [KEY_UP, ord("k")]:
        selected = (selected - 1) % (len(menu_items) or 1)
    elif key in [KEY_DOWN, ord("j")]:
        selected = (selected + 1) % (len(menu_items) or 1)
    return selected


def close_window(stdscr: window, win: window):
    del win
    stdscr.touchwin()
    stdscr.refresh()

from curses import KEY_UP, KEY_DOWN


def check_quit_esc(key):
    if key == 27:
        return True
    if key == ord("q") or key == ord("Q"):
        exit(0)
    return False


def change_selection(key, selected, menu_items):
    if key in [KEY_UP, ord("k")]:
        selected = (selected - 1) % len(menu_items)
    elif key in [KEY_DOWN, ord("j")]:
        selected = (selected + 1) % len(menu_items)
    return selected

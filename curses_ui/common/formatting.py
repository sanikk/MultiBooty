from curses import window, A_REVERSE


def add_reverse(win: window, ln: int, col: int, txt: str):
    win.attron(A_REVERSE)
    win.addstr(ln, col, txt)
    win.attroff(A_REVERSE)


def format_size(size_bytes: int | float):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

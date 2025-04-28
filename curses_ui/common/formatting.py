from curses import window, A_REVERSE

def add_reverse(win: window, ln, col, txt):
    win.attron(A_REVERSE)
    win.addstr(ln, col, txt)
    win.attroff(A_REVERSE)

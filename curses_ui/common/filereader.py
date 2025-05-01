from pathlib import Path
from curses import doupdate, window, newwin, A_REVERSE
# ,KEY_BACKSPACE, KEY_ENTER

from curses_ui.common.controls import change_selection, check_quit_esc
from curses_ui.common.prints import print_key_instructions
# from curses_ui.common.formatting import add_reverse


def filereader(filepath: str, mask: str) -> list:
    files = Path(filepath).glob(mask)
    return list(files)


def close_window(stdscr: window, box_win: window):
    del box_win
    stdscr.touchwin()
    stdscr.refresh()



def fileviewerwindow(stdscr: window, height: int = 22, width: int = 40):
    max_width = stdscr.getmaxyx()[1]
    box_win = newwin(height, width, 1, max_width // 2 - width // 2)
    return box_win

suggested_locations = [
    Path.cwd(),
    Path.home(),
    Path.home() / "Downloads"
]
def listify_path(path: Path|None=None, mask="*"):
    if not path:
        return [(idx, path) for idx,path in enumerate(suggested_locations)]
    return [(idx,entry) for idx,entry in enumerate([entry for entry in path.glob("*") if entry.is_dir() or entry.match(mask)])]

    

def fileviewer(stdscr: window, path: str, mask: str):
    beginning = 0
    showing = 20
    box_win = fileviewerwindow(stdscr=stdscr, height=showing + 5, width=74)
    files = [
        (idx, filepath)
        for idx, filepath in enumerate(filereader(filepath=path, mask=mask))
    ]
    selected = 0
    while True:
        box_win.erase()

        box_win.box()
        max_width = box_win.getmaxyx()[1] - 2
        linenumber = 1
        for idx, file_entry in files[beginning : beginning + showing]:

            if idx == selected:
                box_win.attron(A_REVERSE)
                box_win.addstr(linenumber, 2, f"{str(file_entry)[:max_width]}")
                box_win.attroff(A_REVERSE)
            else:
                box_win.addstr(linenumber, 2, f"{str(file_entry)[:max_width]}")
            linenumber += 1

        print_key_instructions(stdscr=box_win, y_start=linenumber + 1, numbers=False)

        key = box_win.getch()
        if check_quit_esc(key):
            return 0
        selected = change_selection(key, selected=selected, menu_items=files)
        beginning = max(0, min(selected - 10, len(files) - showing))
        box_win.noutrefresh()
        doupdate()


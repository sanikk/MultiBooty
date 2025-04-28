from pathlib import Path
from curses import KEY_BACKSPACE, KEY_ENTER, doupdate, window, newwin, A_REVERSE


from curses_ui.common.controls import change_selection, check_quit_esc
from curses_ui.common.prints import print_key_instructions


def filereader(filepath: str, mask: str) -> list:
    files = Path(filepath).glob(mask)
    return list(files)


def close_window(stdscr: window, box_win: window):
    del box_win
    stdscr.touchwin()
    stdscr.refresh()


def add_reverse(win: window, ln, col, txt):
    win.attron(A_REVERSE)
    win.addstr(ln, col, txt)
    win.attroff(A_REVERSE)

def draw_list(win: window, lst: list, showing: int, selected: int, offset=0):
        max_width = win.getmaxyx()[1] - 2
        linenumber = offset
        beginning = max(0, min(selected - showing // 2, len(lst) - showing))
        for idx, file_entry in lst[beginning : beginning + showing]:
            if idx == selected:
                add_reverse(win, linenumber, 1, f"{str(file_entry)[:max_width]}")
 
            else:
                win.addstr(linenumber, 2, f"{str(file_entry)[:max_width]}")
            linenumber += 1
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

    
def draw_picked_view(win: window, lst: list, selected: int):
    max_y, max_x = win.getmaxyx()
    add_reverse(win, 0,0, "Picked files:")
    draw_list(win, lst=lst, showing=max_y - 4, selected=selected, offset=2)

def draw_dir_view(win: window, current: str, lst: list, selected: int):
    max_y, max_x = win.getmaxyx()
    showing = max_y - 5
    add_reverse(win, 0, 0, current)
    draw_list(win=win, lst=lst, showing=showing, selected=selected, offset=1)
    win.refresh()

def picker_windows(stdscr: window, height=None, width=None):
    frame_max_y, frame_max_x = stdscr.getmaxyx()
    height = height or frame_max_y - 5
    width = width or frame_max_x - 5
    if width % 2 == 0:
        width += 1
    whole_window = newwin(height, width, frame_max_y // 2 - height // 2, frame_max_x // 2 - width // 2)
    max_y, max_x = stdscr.getmaxyx()
    left_pane = whole_window.derwin(max_y - 2, max_x // 2 - 1, 1 ,1)
    right_pane = whole_window.derwin(max_y - 2, max_x // 2 - 1, 1, max_x // 2 + 1)

    selected_pane = 0

    left_list = listify_path()
    left_cwd = None
    left_selected = 0

    right_list = []
    right_selected = 0

    while True:
        whole_window.erase()
        left_text = left_cwd.__str__() if left_cwd else "Suggested locations"
        draw_dir_view(win=left_pane, current=left_text, lst=left_list, selected=left_selected)
        draw_picked_view(win=right_pane, lst=right_list, selected=right_selected)

        key = whole_window.getch()
        if check_quit_esc(key=key):
            return 0
        if selected_pane:
            right_selected = change_selection(key, right_selected, right_list)
            if key in (KEY_BACKSPACE, 8, 127):
                pass
            elif key in (KEY_ENTER, 10, 13):
                pass
            elif key == 9:
                selected_pane = 0
        else:
            left_selected = change_selection(key, left_selected, left_list)
            if key in (KEY_BACKSPACE, 8, 127):
            
                if left_cwd and left_cwd != Path.home():
                    left_cwd = left_cwd.parent
                else:
                    left_cwd = None
            elif key in (KEY_ENTER, 10, 13):
                pass
            elif key == 9:
                selected_pane = 1
def fileviewer(stdscr: window, path: str, mask: str):
    # return a new window with height = 25, width = 40, start_y = 1, start_x=stdscr.getmaxyx()[1] // 2 - width // 2
    beginning = 0
    showing = 20
    box_win = fileviewerwindow(stdscr=stdscr, height=showing + 5, width=74)
    files = [
        (idx, filepath)
        # filereader returns list[Path]
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
        # return true if esc, sys.exit on q
        if check_quit_esc(key):
            return 0
        # returns selection - 1 % len(menu_items) - 1 for k, returns selection + 1 % len(menu_items) - 1 for j
        selected = change_selection(key, selected=selected, menu_items=files)
        beginning = max(0, min(selected - 10, len(files) - showing))
        box_win.noutrefresh()
        doupdate()


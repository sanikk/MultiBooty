from pathlib import Path
from curses import doupdate, window, newwin, KEY_ENTER, KEY_BACKSPACE

from curses_ui.common.formatting import add_reverse
from curses_ui.common.prints import print_file_list
from curses_ui.common.filereader import listify_path
from curses_ui.common.controls import change_selection, check_quit_esc


def draw_picked_view(win: window, lst: list, selected: int):
    max_y, max_x = win.getmaxyx()
    add_reverse(win, 0, 0, "Picked files:")
    win.hline(1, 0, "-", max_x)
    print_file_list(
        win, lst=lst, showing=max_y - 4, selected=selected, y_offset=2, x_offset=2
    )


def draw_dir_view(win: window, current: str, lst: list, selected: int):
    max_y, max_x = win.getmaxyx()
    showing = max_y - 5
    add_reverse(win, 0, 0, current)
    win.hline(1, 0, "-", max_x)
    print_file_list(
        win=win, lst=lst, showing=showing, selected=selected, y_offset=2, x_offset=2
    )
    win.refresh()


def picker_windows(stdscr: window, height: int | None = None, width: int | None = None):
    frame_max_y, frame_max_x = stdscr.getmaxyx()
    height = height or frame_max_y - 5
    width = width or frame_max_x - 5
    if width % 2 == 0:
        width += 1
    whole_window = newwin(
        height, width, frame_max_y // 2 - height // 2, frame_max_x // 2 - width // 2
    )
    max_y, max_x = whole_window.getmaxyx()
    left_pane = whole_window.derwin(max_y - 2, max_x // 2 - 1, 1, 1)
    right_pane = whole_window.derwin(max_y - 2, max_x // 2 - 1, 1, max_x // 2 + 1)

    selected_pane = 0

    left_list = listify_path()
    left_cwd = None
    left_selected = 0

    right_list = []
    right_selected = 0

    while True:
        whole_window.erase()
        whole_window.box()
        left_text = left_cwd.__str__() if left_cwd else "Suggested locations"
        draw_dir_view(
            win=left_pane, current=left_text, lst=left_list, selected=left_selected
        )
        draw_picked_view(win=right_pane, lst=right_list, selected=right_selected)
        whole_window.vline(1, width // 2, "|", max_y - 2)

        key = whole_window.getch()
        if check_quit_esc(key=key):
            return 0
        if selected_pane:  # on right pane
            right_selected = change_selection(key, right_selected, right_list)
            if key in (KEY_BACKSPACE, 8, 127):
                pass
            elif key in (KEY_ENTER, 10, 13):
                pass
            elif key == 9:
                selected_pane = 0
        else:  # on left pane
            left_selected = change_selection(key, left_selected, left_list)
            if key in (KEY_BACKSPACE, 8, 127):

                if left_cwd and left_cwd != Path.home():
                    left_cwd = left_cwd.parent
                else:
                    left_cwd = None
                left_list = listify_path(left_cwd)
            elif key in (KEY_ENTER, 10, 13):
                selected_entry = left_list[left_selected][1]
                if selected_entry.is_dir():
                    left_cwd = selected_entry
                    left_list = listify_path(left_cwd)
                elif selected_entry.is_file():
                    right_list.append((len(right_list), selected_entry))
            elif key == 9:
                selected_pane = 1

        whole_window.noutrefresh()
        doupdate()

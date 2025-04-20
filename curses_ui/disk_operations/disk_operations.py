from curses import window, KEY_ENTER
from curses_ui.common.controls import change_selection
from curses_ui.common.prints import print_key_instructions, print_top, print_menu
from curses_ui.common.controls import check_quit_esc
from curses_ui.disk_operations.partition_disk import partition_disk
from disk_ops.device_service import DeviceService


def disk_operations(stdscr: window, device_service: DeviceService, **_):
    menu_items = [
        "Partition disk",
        "Install grub",
        "Make folders on root",
    ]
    selected = 0
    while True:
        stdscr.clear()
        stdscr.refresh()

        print_top(stdscr=stdscr, device_service=device_service)

        print_menu(stdscr=stdscr, menu_items=menu_items, selected=selected)

        print_key_instructions(stdscr=stdscr)

        key = stdscr.getch()

        if check_quit_esc(key):
            return 0
        selected = change_selection(key=key, selected=selected, menu_items=menu_items)
        if (key in [KEY_ENTER, 10, 13] and selected == 0) or key == ord("1"):
            partition_disk(stdscr=stdscr, device_service=device_service)
        if (key in [KEY_ENTER, 10, 13] and selected == 1) or key == ord("2"):
            # TODO: implement this
            pass
        if (key in [KEY_ENTER, 10, 13] and selected == 2) or key == ord("3"):
            # TODO: implement this
            pass

from curses import window, KEY_ENTER

from curses_ui.common.filereader import fileviewer
from curses_ui.common.prints import print_key_instructions, print_menu, print_top
from curses_ui.common.controls import check_quit_esc, change_selection
from disk_ops.device_service import DeviceService
from grub.grub_service import GrubService


def iso_bootloader_management(
    stdscr: window, device_service: DeviceService, grub_service: GrubService
):
    menu_items = [
        "file viewer",
        # "Install grub",
        # "Make folders on root",
    ]
    selected = 0
    while True:
        stdscr.clear()
        stdscr.refresh()

        print_top(stdscr=stdscr, device_service=device_service)

        print_menu(stdscr=stdscr, menu_items=menu_items, selected=selected)

        print_key_instructions(stdscr=stdscr, y_offset=len(menu_items) // 2 + 2)

        key = stdscr.getch()

        if check_quit_esc(key):
            return 0
        selected = change_selection(key=key, selected=selected, menu_items=menu_items)
        if (key in [KEY_ENTER, 10, 13] and selected == 0) or key == ord("1"):
            fileviewer(stdscr=stdscr, path="/home/karpo/", mask="*.*")
        if (key in [KEY_ENTER, 10, 13] and selected == 1) or key == ord("2"):
            # TODO: implement this
            pass
        if (key in [KEY_ENTER, 10, 13] and selected == 2) or key == ord("3"):
            # TODO: implement this
            pass

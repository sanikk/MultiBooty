from curses import window, KEY_ENTER
from curses_ui.common.controls import change_selection
from curses_ui.common.prints import print_key_instructions, print_top, print_menu
from curses_ui.common.controls import check_quit_esc
from curses_ui.disk_operations.partition_disk import partition_disk
from curses_ui.disk_operations.install_file_systems import install_file_systems

# from curses_ui.disk_operations.install_grub import install_grub
from disk_ops.device_service import DeviceService


def disk_operations(stdscr: window, device_service: DeviceService, **_):
    menu_items = [
        "Partition disk",
        "Install file systems",
        "Install grub",
        "Make folders on root",
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
            partition_disk(stdscr=stdscr, device_service=device_service)
        elif (key in [KEY_ENTER, 10, 13] and selected == 1) or key == ord("2"):
            install_file_systems(stdscr=stdscr, device_service=device_service)
        elif (key in [KEY_ENTER, 10, 13] and selected == 2) or key == ord("3"):
            # install_grub(stdscr=stdscr, grub_service=grub_service)
            pass
            # TODO: implement this
        elif (key in [KEY_ENTER, 10, 13] and selected == 2) or key == ord("3"):
            pass

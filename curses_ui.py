from sys import exit
from curses_ui.select_device.select_device import select_device

from curses_ui.show_device_info import show_device_info_screen
from curses_ui.install_grub import install_grub_screen

from curses_ui.utils import check_quit_esc
from curses_ui.common.prints import print_key_instructions, print_menu, print_top
from disk_ops.device_service import DeviceService
from grub.grub_service import GrubService
from curses import window, wrapper, curs_set, KEY_UP, KEY_DOWN, KEY_ENTER


def fake_func():
    # replace this with actual function
    pass


menu_items = [
    ("Select Target Device", select_device),
    ("Disk Operations", show_device_info_screen),
    ("Install / Manage MultiBooty", install_grub_screen),
    ("ISO & Bootloader Setup", fake_func),
    ("Package Cache Management", fake_func),
]


def main_menu(stdscr: window, device_service: DeviceService, grub_service: GrubService):
    curs_set(0)
    selected = 0
    stdscr.clear()
    while True:
        print_top(stdscr=stdscr, device_service=device_service)

        print_menu(stdscr=stdscr, menu_items=menu_items, selected=selected)

        stdscr.addstr("\n\n")

        print_key_instructions(stdscr=stdscr)
        stdscr.refresh()

        key = stdscr.getch()
        if not check_quit_esc(key):
            exit(0)
        if key in [KEY_UP, ord("k")]:
            selected = (selected - 1) % len(menu_items)
        elif key in [KEY_DOWN, ord("j")]:
            selected = (selected + 1) % len(menu_items)
        elif key in [KEY_ENTER, 10, 13]:
            selected = menu_items[selected][1](
                stdscr=stdscr, device_service=device_service, grub_service=grub_service
            )
        elif key in map(ord, "123456"):
            menu_items[(key - ord("0"))][1](
                stdscr=stdscr, device_service=device_service, grub_service=grub_service
            )


if __name__ == "__main__":
    device_service = DeviceService()
    grub_service = GrubService(device_service)
    wrapper(main_menu, device_service=device_service, grub_service=grub_service)

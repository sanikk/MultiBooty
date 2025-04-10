import curses
import sys
from curses_ui.select_block_device import select_block_device_screen
from curses_ui.show_device_info import show_device_info_screen
from curses_ui.install_grub import install_grub_screen
from curses_ui.configure_grub import configure_grub_screen
from curses_ui.utils import check_quit_esc

from disk_ops.device_service import DeviceService
from grub.grub_service import GrubService

menu_items = [
    ("Select device", select_block_device_screen),
    ("Partitioning", show_device_info_screen),
    ("Install GRUB", install_grub_screen),
    # ("Install MultiBooty", install_multibooty_screen),
    # ("Configure GRUB", configure_grub_screen),
]


def main_menu(stdscr, device_service: DeviceService, grub_service: GrubService):
    curses.curs_set(0)  # Hide cursor
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(f"Device: {device_service.get_device()}\n")
        stdscr.addstr(f"Number of sectors: {device_service.get_number_of_sectors()}\n")
        h, w = stdscr.getmaxyx()

        for idx, (item, func) in enumerate(menu_items):
            x = w // 2 - len(item) // 2
            y = h // 2 - len(menu_items) // 2 + idx
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item)

        stdscr.refresh()

        key = stdscr.getch()
        if not check_quit_esc(key):
            sys.exit(0)
        if key in [curses.KEY_UP, ord("k")]:
            selected = (selected - 1) % len(menu_items)
        elif key in [curses.KEY_DOWN, ord("j")]:
            selected = (selected + 1) % len(menu_items)
        elif key in [curses.KEY_ENTER, 10, 13]:
            selected = menu_items[selected][1](
                stdscr=stdscr, device_service=device_service, grub_service=grub_service
            )


if __name__ == "__main__":
    device_service = DeviceService()
    grub_service = GrubService(device_service)
    curses.wrapper(main_menu, device_service=device_service, grub_service=grub_service)

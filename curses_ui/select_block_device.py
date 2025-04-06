from disk_ops.disks.block_devices import get_all_block_devices
from disk_ops.disks.disk_runners import get_disk_info
from curses_ui.utils import format_size
import sys


def select_block_device_screen(stdscr, device=None):
    """
    This is first screen.

    """
    stdscr.clear()
    disk_info = get_disk_info(get_all_block_devices())
    devices = [(k, *v.values()) for k, v in disk_info.items()]

    stdscr.addstr(0, 0, "dev          sector size  number of sectors  total size\n")
    # stdscr.addstr(f"{devices=}\n")
    stdscr.addstr("----------------------------------------------------------\n")

    for i, (dev, sector_size, num_sectors, size_bytes) in enumerate(devices, 1):
        size_str = format_size(size_bytes)
        stdscr.addstr(f"{i}. {dev:12} {sector_size:12} {num_sectors:16} {size_str}\n")

    stdscr.addstr("\nEnter a device number or 'q' to quit: ")

    while True:
        char = stdscr.getch()

        if char == ord("q"):
            sys.exit(0)

        try:
            selected_device_index = int(chr(char)) - 1
            if devices:
                selected_device = devices[selected_device_index]
                return 1, selected_device[0]
        except (ValueError, IndexError):
            stdscr.addstr(
                "\nInvalid selection. Please enter a valid number or 'q' to quit.\n"
            )
            stdscr.refresh()

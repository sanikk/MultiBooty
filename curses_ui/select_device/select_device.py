from curses import window
from curses_ui.common.prints import print_key_instructions, print_top
from disk_ops.device_service import DeviceService
from curses_ui.utils import check_quit_esc, format_size


def select_device(stdscr: window, device_service, **kwargs):
    _ = kwargs

    selected = 0

    while True:
        stdscr.clear()
        print_top(stdscr=stdscr, device_service=device_service)

        disk_info = device_service.list_devices()
        devices = [(k, *v.values()) for k, v in disk_info.items()]

        stdscr.addstr(
            3, 0, "#  dev          sector size  number of sectors  total size\n"
        )
        stdscr.addstr("----------------------------------------------------------\n")

        for i, (dev, sector_size, num_sectors, size_bytes) in enumerate(devices, 1):
            size_str = format_size(size_bytes)
            stdscr.addstr(
                f"{i}. {dev:12} {sector_size:12} {num_sectors:16} {size_str}\n"
            )
        char = stdscr.getch()
        # TODO: handle char

        if not check_quit_esc(char):
            return 0
        try:
            selected_device_index = int(chr(char)) - 1
            if devices:
                device_service.set_device(*devices[selected_device_index])
                return 1
        except (ValueError, IndexError):
            stdscr.addstr(
                "\nInvalid selection. Please enter a valid number, 'esc' to return or 'q' to quit.\n"
            )
            stdscr.refresh()

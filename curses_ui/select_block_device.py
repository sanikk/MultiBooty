from disk_ops.device_service import DeviceService
from curses_ui.utils import check_quit_esc, format_size


def select_block_device_screen(stdscr, device_service: DeviceService):
    """
    This is first screen.
    User can select a usb device here.

    Args:
        device_service (DeviceService): device service to use

    Returns:
        next_screen (int): index of next screen

    """
    stdscr.clear()
    stdscr.refresh()
    disk_info = device_service.list_devices()
    stdscr.clear()
    stdscr.refresh()
    devices = [(k, *v.values()) for k, v in disk_info.items()]

    stdscr.addstr(0, 0, "dev          sector size  number of sectors  total size\n")
    stdscr.addstr("----------------------------------------------------------\n")

    for i, (dev, sector_size, num_sectors, size_bytes) in enumerate(devices, 1):
        size_str = format_size(size_bytes)
        stdscr.addstr(f"{i}. {dev:12} {sector_size:12} {num_sectors:16} {size_str}\n")

    stdscr.addstr("\nEnter a device number, 'esc' to return or 'q' to quit: ")
    stdscr.refresh()

    while True:
        char = stdscr.getch()

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

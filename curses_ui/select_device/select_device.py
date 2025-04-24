from curses import window
from curses_ui.common.prints import print_disk_entry, print_key_instructions, print_top
from disk_ops.device_service import DeviceService
from curses_ui.common.controls import check_quit_esc


def select_device(stdscr: window, device_service: DeviceService, **kwargs):
    _ = kwargs

    while True:
        stdscr.clear()
        stdscr.refresh()

        disk_info = device_service.list_devices()

        stdscr.clear()
        stdscr.refresh()

        print_top(stdscr=stdscr, device_service=device_service)

        stdscr.addstr(
            f"{"#":3} {"dev":10} {"start":13} {"end":10} {"sectors":8} {"size":8} {"fstype":10} {"label":10}\n"
        )
        stdscr.addstr("-" * 80 + "\n")
        if not disk_info:
            stdscr.addstr("No removable devices found.")
        else:
            for i, disk_entry in enumerate(disk_info):
                print_disk_entry(stdscr=stdscr, disk_entry=disk_entry, i=i)

        print_key_instructions(stdscr=stdscr, updown=False)

        char = stdscr.getch()

        if check_quit_esc(char):
            return 0
        try:
            as_number = char - ord("0")
            if as_number in range(1, len(disk_info) + 1):
                device_service.set_device(as_number - 1)
                return 1
        except (ValueError, IndexError):
            stdscr.addstr(
                "\nInvalid selection. Please enter a valid number, 'esc' to return or 'q' to quit.\n"
            )
            stdscr.getch()
            stdscr.refresh()

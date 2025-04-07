from curses_ui.utils import check_quit_esc
from disk_ops.device_service import DeviceService
from disk_ops.disks.gather_block_info import gather_block_info
import curses
import sys


def show_partitions(stdscr, device_service):
    device_info = gather_block_info(device_service.get_device())
    if not device_info:
        stdscr.addstr("No device found.\n")
        stdscr.addstr("Press any key to continue...")
        stdscr.getch()
        return False

    stdscr.addstr(f"Selected Device: /dev/{device_info['name']}\n")
    stdscr.addstr(
        f"{'Identifier':<15}{'Name':<32}{'FS':<12}{'Size':<10}{'Mount Points'}\n"
    )
    stdscr.addstr("-" * 80 + "\n")

    stdscr.addstr(
        f"/dev/{device_info['name']:<14}{(device_info['vendor'] or '') + ' ' + (device_info['model'] or ''):<30}"
        f"{device_info['fstype'] or 'Unknown':<10}{device_info['size']:<10}"
        f"{'Unknown':<10}{', '.join(m if m else 'None' for m in device_info['mountpoints'])}\n"
    )

    if "children" in device_info and device_info["children"]:
        for idx, part in enumerate(device_info["children"]):
            stdscr.addstr(
                f"  └ {idx:<12}{(part['label'] or part['partname'] or 'Unknown'):<30}"
                f"{part['fstype'] or 'Unknown':<10}{part['size']:<10}"
                f"{'Unknown':<10}{', '.join(m if m else 'None' for m in part['mountpoints'])}\n"
            )
    return True


def suggest_partitions(stdscr, device_service, boot_size_mb):
    partitions_info = device_service.suggest_partitions(boot_size_mb)
    stdscr.addstr(
        "\nPartition   Name                                 Start        End          Size (MB)    File System    Bootable\n"
    )
    stdscr.addstr("-" * 90 + "\n")

    for idx, part in enumerate(partitions_info["partitions"]):
        bootable = "Y" if idx == 0 else " "
        stdscr.addstr(
            f"{idx:<10}{part['name']:<35}{part['start']:<12}{part['end']:<12}{part['size_mb']:<12.2f}{part['type']:<15}{bootable}\n"
        )
    stdscr.addstr(
        "\nThis will get written to disk. Press 'Y' to confirm, 'Escape' to return, or 'q' to quit.\n"
    )
    while True:
        key = stdscr.getch()
        if not check_quit_esc(key):
            return False
        if key == ord("Y"):
            stdscr.addstr(f"Partitioning {partitions_info["device"]}...\n")
            device_service.make_partitions()
            return True
        stdscr.refresh()


def show_device_info_screen(stdscr, device_service: DeviceService):
    """
    Second screen
    User can see the current partitioning for the device, and enter a desired boot partition size.

    """
    stdscr.clear()
    curses.curs_set(1)
    ret = show_partitions(stdscr, device_service)
    stdscr.addstr("\nPress 'esc' to pick another block device, 'q' to quit\n")
    if ret:
        stdscr.addstr("or Enter boot partition size in MB (default 100MB): ")
    stdscr.refresh()

    boot_size_str = ""
    while True:
        key = stdscr.getch()

        if key == 27:
            return 0

        elif key == ord("q"):
            sys.exit(0)
        elif key in (10, curses.KEY_ENTER):
            boot_size_mb = None
            if boot_size_str and boot_size_str.isdigit():
                boot_size_mb = int(boot_size_str)
            else:
                boot_size_mb = 100
            if suggest_partitions(stdscr, device_service, boot_size_mb):
                stdscr.clear()
                if show_partitions(stdscr, device_service):
                    stdscr.addstr("\nPress any key to continue..")
                    stdscr.getch()
                return 2
            return 0

        elif key in range(48, 58):  # Number keys 0-9
            boot_size_str += chr(key)
            stdscr.addch(chr(key))

        elif key in (127, curses.KEY_BACKSPACE, 8) and boot_size_str:
            boot_size_str = boot_size_str[:-1]
            y, x = stdscr.getyx()
            if x > 0:
                stdscr.move(y, x - 1)
                stdscr.delch()

        stdscr.refresh()

from typing import no_type_check
from disk_ops.disks.block_devices import get_all_block_devices
from disk_ops.disks.disk_runners import get_disk_info
from disk_ops.disks.gather_block_info import gather_block_info

from disk_ops.partitions.partition_runners import (
    propose_partitions,
    make_partitions,
)
from disk_ops.make_filesystems import (
    make_boot_filesystem,
    make_ext_filesystem,
)
import sys
import curses


def partition_disk(stdscr, dev, boot_start, boot_end, root_start, root_end):
    stdscr.addstr(f"Partitioning {dev}...")
    make_partitions(dev, boot_start, boot_end, root_start, root_end)
    stdscr.addstr(f"Making fat32 filesystem for {dev} boot partition.")
    make_boot_filesystem(dev, 1)
    stdscr.addstr(f"Making ext4 filesystem for {dev} root partition.")
    make_ext_filesystem(dev, 2)
    stdscr.addstr(f"Boot partition: {boot_start=}, {boot_end=}")
    stdscr.addstr(f"Root partition: {root_start=}, {root_end=}")
    stdscr.addstr("Press any key to continue...")
    stdscr.getch()
    return (None,)


def something_went_wrong(stdscr):
    stdscr.addstr("Something went wrong\n")
    stdscr.addstr("Press any key to continue...")
    stdscr.getch()


def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def select_block_device_screen(stdscr):
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
                return show_current_partitions_screen, selected_device[0]
        except (ValueError, IndexError):
            stdscr.addstr(
                "\nInvalid selection. Please enter a valid number or 'q' to quit.\n"
            )
            stdscr.refresh()


def show_current_partitions_screen(stdscr, selected_device: str):
    curses.curs_set(1)

    device_info = gather_block_info(selected_device)
    if not device_info:
        stdscr.addstr("No device found.\n")
        stdscr.addstr("Press any key to continue...")
        stdscr.getch()
        return (select_block_device_screen,)

    stdscr.addstr(f"Selected Device: /dev/{device_info['name']}\n")
    stdscr.addstr(
        f"{'Identifier':<15}{'Name':<32}{'FS':<12}{'Size':<10}{'Unused':<10}{'Mount Points'}\n"
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

    stdscr.addstr("\nEnter boot partition size in MB (default 100MB): ")
    stdscr.refresh()

    boot_size_str = ""
    while True:
        key = stdscr.getch()

        if key == 27:
            return (select_block_device_screen,)

        elif key == ord("q"):
            sys.exit(0)

        elif key in (10, curses.KEY_ENTER):
            boot_size_mb = None
            if boot_size_str and boot_size_str.isdigit():
                boot_size_mb = int(boot_size_str)
            else:
                boot_size_mb = 100
            return new_partitions_screen, selected_device, boot_size_mb

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


@no_type_check
def new_partitions_screen(stdscr, dev: str, boot_size_mb: int):
    """
    Shows the suggested partitioning scheme to the user.

    @no_type_check because pyright does not play nice with JSON here.
    """
    partitions_info = propose_partitions(dev, boot_size_mb)
    if "error" in partitions_info:
        something_went_wrong(stdscr)
        return (select_block_device_screen,)
    alignment = partitions_info["alignment"]
    grain_size = alignment["minimum_grain_size"]

    stdscr.addstr(f"Device: {partitions_info['device']}\n")
    stdscr.addstr(f"Sector size: {partitions_info['sector_size']}\n")
    stdscr.addstr(f"Number of sectors: {partitions_info['total_sectors']}\n")
    stdscr.addstr(f"Total size: {partitions_info['disk_size_mb']} MB\n")
    stdscr.addstr(f"Alignment Grain size: {grain_size}\n")

    if (
        alignment["align_down_test_1025"] != 0
        or alignment["align_up_test_1025"] != grain_size
    ):
        stdscr.addstr(
            "Warning! Grain size does not match reported\n",
            curses.A_BOLD | curses.A_REVERSE,
        )

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
        if key == 27:
            return show_current_partitions_screen, dev
        elif key == ord("q"):
            sys.exit(0)
        elif key == ord("Y"):
            boot_start = partitions_info["partitions"][0]["start"]
            boot_end = partitions_info["partitions"][0]["end"]
            root_start = partitions_info["partitions"][1]["start"]
            root_end = partitions_info["partitions"][1]["end"]
            return partition_disk, dev, boot_start, boot_end, root_start, root_end
        stdscr.refresh()


def main_loop(stdscr):
    next_func = select_block_device_screen
    args = []
    while next_func:
        stdscr.clear()
        next_func, *args = next_func(stdscr, *args)
    sys.exit(0)


if __name__ == "__main__":
    curses.wrapper(main_loop)

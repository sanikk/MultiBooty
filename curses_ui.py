from disk_ops.block_devices import get_all_block_devices
from disk_ops.disk_info import get_disk_info
import curses


def get_partition_info(dev):
    return [
        {"partition": "/dev/sdc1", "size": 5000000000},
        {"partition": "/dev/sdc2", "size": 5000000000},
    ]


def partition_disk(dev):
    print(f"Partitioning {dev}...")


def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def run_ui(stdscr):
    stdscr.clear()

    devices = get_disk_info(get_all_block_devices())

    stdscr.addstr(0, 0, "dev          sector size  number of sectors  total size\n")
    stdscr.addstr("----------------------------------------------------------\n")

    for i, (dev, info) in enumerate(devices.items(), 1):
        size_str = format_size(info["size_bytes"])
        stdscr.addstr(
            f"{i}. {dev:12} {info['sector_size']:12} {info['num_sectors']:16} {size_str}\n"
        )

    stdscr.addstr("\nEnter a device number or 'q' to quit: ")

    while True:
        char = stdscr.getch()

        if char == ord("q"):
            break

        try:
            selected_device_index = int(chr(char)) - 1
            selected_device = list(devices.keys())[selected_device_index]

            partitions = get_partition_info(selected_device)

            stdscr.clear()
            stdscr.addstr(f"Selected Device: {selected_device}\n")
            stdscr.addstr("Partitions:\n")

            for partition in partitions:
                stdscr.addstr(
                    f" - {partition['partition']} ({format_size(partition['size'])})\n"
                )

            stdscr.addstr("\nWarning: The disk will be wiped. Are you sure? (Y/N): ")
            stdscr.refresh()

            confirmation = stdscr.getch()
            if chr(confirmation).lower() == "y":
                partition_disk(selected_device)
                stdscr.addstr("\nDisk partitioned successfully!\n")
            else:
                stdscr.addstr("\nOperation canceled.\n")

            stdscr.addstr("\nPress any key to continue...")
            stdscr.getch()

            break

        except (ValueError, IndexError):
            stdscr.addstr(
                "\nInvalid selection. Please enter a valid number or 'q' to quit.\n"
            )
            stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(run_ui)

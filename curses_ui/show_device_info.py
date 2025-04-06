from disk_ops.disks.gather_block_info import gather_block_info
import curses
import sys


def show_device_info_screen(stdscr, selected_device: str, new_partition: bool = True):
    curses.curs_set(1)

    device_info = gather_block_info(selected_device)
    if not device_info:
        stdscr.addstr("No device found.\n")
        stdscr.addstr("Press any key to continue...")
        stdscr.getch()
        return (0,)

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

    if new_partition:
        stdscr.addstr("\nEnter boot partition size in MB (default 100MB): ")
        stdscr.refresh()
    else:
        stdscr.addstr(
            "Press 'enter' to continue, 'esc' to pick another block device and 'q' to quit"
        )

    boot_size_str = ""
    while True:
        key = stdscr.getch()

        if key == 27:
            return (0,)

        elif key == ord("q"):
            sys.exit(0)
        elif key in (10, curses.KEY_ENTER):
            if new_partition:
                boot_size_mb = None
                if boot_size_str and boot_size_str.isdigit():
                    boot_size_mb = int(boot_size_str)
                else:
                    boot_size_mb = 100
                return new_partitions_screen, selected_device, boot_size_mb
            else:
                return grub_screen, selected_device

        elif new_partition and key in range(48, 58):  # Number keys 0-9
            boot_size_str += chr(key)
            stdscr.addch(chr(key))

        elif new_partition and key in (127, curses.KEY_BACKSPACE, 8) and boot_size_str:
            boot_size_str = boot_size_str[:-1]
            y, x = stdscr.getyx()
            if x > 0:
                stdscr.move(y, x - 1)
                stdscr.delch()

        stdscr.refresh()

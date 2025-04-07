import curses


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

            stdscr.addstr(f"Partitioning {dev}...\n")
            make_partitions(dev, boot_start, boot_end, root_start, root_end)
            return partition_disk, dev, boot_start, boot_end, root_start, root_end
        stdscr.refresh()

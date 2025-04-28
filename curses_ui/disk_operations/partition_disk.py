from curses import KEY_ENTER, window
from curses_ui.common.controls import change_selection, check_quit_esc
from curses_ui.common.prints import (
    print_disk_entry,
    print_key_instructions,
    print_menu,
    print_top,
)
from curses_ui.common.prompts import selection_box, text_prompt
from disk_ops.device_service import DeviceService


def partition_disk(stdscr: window, device_service: DeviceService, **kwargs):
    _ = kwargs

    boot_size = 100
    selected = 0
    stdscr.clear()
    stdscr.refresh()
    device_info = device_service.get_device()

    if not device_info:
        stdscr.addstr("No device found.\n")
        stdscr.addstr("Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()
        return 1

    while True:
        stdscr.clear()
        stdscr.refresh()
        print_top(stdscr=stdscr, device_service=device_service)
        print_disk_entry(stdscr=stdscr, disk_entry=device_info)

        menu_items = [
            f"Boot partition size: {boot_size:4} MB",
            f"Boot partition file system: {device_service.get_boot_fs()}",
            f"Root partition size: rest of the disk",
            f"Root partition file system: {device_service.get_root_fs()}",
            "Partition disk",
        ]
        print_menu(stdscr=stdscr, menu_items=menu_items, selected=selected)

        print_key_instructions(stdscr=stdscr, y_offset=len(menu_items) // 2 + 2)

        key = stdscr.getch()
        if check_quit_esc(key):
            return 1
        selected = change_selection(key=key, selected=selected, menu_items=menu_items)
        if (key in (10, KEY_ENTER) and selected == 0) or key == ord("1"):
            y, x = stdscr.getmaxyx()
            y = y // 2 - len(menu_items) // 2
            x = x // 2 + 10
            ret = text_prompt(stdscr, y, x)
            if ret and ret.isdigit():
                boot_size = int(ret)
        elif (key in (10, KEY_ENTER) and selected == 1) or key == ord("2"):

            selection_box(
                stdscr=stdscr,
                message=["Please select a file system", "for the boot partition."],
                choices=device_service.get_boot_fs_types(),
                callback=device_service.set_boot_fs,
                default_index=0,
            )

        elif (key in (10, KEY_ENTER) and selected == 3) or key == ord("4"):

            selection_box(
                stdscr=stdscr,
                message=["Please select a file system", "for the root partition."],
                choices=device_service.get_root_fs_types(),
                callback=device_service.set_root_fs,
                default_index=0,
            )
        elif (key in (10, KEY_ENTER) and selected == 4) or key == ord("5"):
            device_service.partition_disk()


# def show_partitions(stdscr, device_service: DeviceService):
#     # HACK: ok this is terrible. complete rewrite needed.
#     device_info = device_service.device_info()
#     # stdscr.addstr(f"{device_info=}\n")
#     if not device_info:
#         stdscr.addstr("No device found.\n")
#         stdscr.addstr("Press any key to continue...")
#         stdscr.getch()
#         return False
#
#     stdscr.addstr(f"Selected Device: /dev/{device_info['name']}\n")
#     stdscr.addstr(
#         f"{'Identifier':<15}{'Name':<32}{'FS':<12}{'Size':<10}{'Mount Points'}\n"
#     )
#     stdscr.addstr("-" * 80 + "\n")
#
#     stdscr.addstr(
#         f"/dev/{device_info['name']:<14}{(device_info['vendor'] or '') + ' ' + (device_info['model'] or ''):<30}"
#         f"{device_info['fstype'] or 'Unknown':<10}{device_info['size']:<10}"
#         f"{'Unknown':<10}{', '.join(m if m else 'None' for m in device_info['mountpoints'])}\n"
#     )
#
#     if "children" in device_info and device_info["children"]:
#         for idx, part in enumerate(device_info["children"]):
#             stdscr.addstr(
#                 f"  └ {idx:<12}{(part['label'] or part['partname'] or 'Unknown'):<30}"
#                 f"{part['fstype'] or 'Unknown':<10}{part['size']:<10}"
#                 f"{'Unknown':<10}{', '.join(m if m else 'None' for m in part['mountpoints'])}\n"
#             )
#     stdscr.refresh()
#     return True


# def suggest_partitions(stdscr, device_service, boot_size_mb):
#     partitions_info = device_service.suggest_partitions(boot_size_mb)
#     stdscr.addstr(
#         "\nPartition   Name                                 Start        End          Size (MB)    File System    Bootable\n"
#     )
#     stdscr.addstr("-" * 90 + "\n")
#
#     for idx, part in enumerate(partitions_info["partitions"]):
#         bootable = "Y" if idx == 0 else " "
#         stdscr.addstr(
#             f"{idx:<10}{part['name']:<35}{part['start']:<12}{part['end']:<12}{part['size_mb']:<12.2f}{part['type']:<15}{bootable}\n"
#         )
#     stdscr.addstr(
#         "\nThis will get written to disk. Press 'Y' to confirm, 'Escape' to return, or 'q' to quit.\n"
#     )
#     stdscr.refresh()
#     while True:
#         key = stdscr.getch()
#         if not check_quit_esc(key):
#             return False
#         if key == ord("Y"):
#             stdscr.addstr(f"Partitioning {partitions_info["device"]}...\n")
#             stdscr.refresh()
#             device_service.make_partitions()
#             return True
#         stdscr.refresh()


# def show_device_info_screen(
#     stdscr, device_service: DeviceService, grub_service: GrubService
# ):
#     """
#     Second screen
#     User can see the current partitioning for the device, and enter a desired boot partition size.
#
#     """
#     stdscr.clear()
#     ret = show_partitions(stdscr, device_service)
#     if not ret:
#         return
#     boot_size = 100
#     boot_fs = "fat32"
#     root_fs = "ext4 no journaling"
#     selected = 4
#
#     while True:
#
#         options = [
#             f"Boot partition size: {boot_size} MB",
#             f"Boot partition file system: {boot_fs}",
#             f"Root partition size: rest of the disk",
#             f"Root partition file system: {root_fs}",
#             "Partition disk",
#         ]
#
#         for idx, label in enumerate(options):
#             attr = curses.A_REVERSE if idx == selected else curses.A_NORMAL
#             stdscr.addstr(7 + idx, 2, label, attr)
#
#         print_key_instructions(stdscr)
#
#         key = stdscr.getch()
#
#         if key == 27:
#             return 0
#
#         elif key == ord("q"):
#             sys.exit(0)
#
#         elif key in (curses.KEY_UP, ord("k")):
#             selected = (selected - 1) % len(options)
#         elif key in (curses.KEY_DOWN, ord("j")):
#             selected = (selected + 1) % len(options)
#
#         elif key in (10, curses.KEY_ENTER):
#             if selected == 0:
#                 ret = text_prompt(stdscr, 7, 22)
#                 if ret and ret.isdigit():
#                     boot_size = int(ret)
#             if selected == 4:
#                 if suggest_partitions(stdscr, device_service, boot_size):
#                     stdscr.addstr("Partitioning done.\n")
#                     stdscr.addstr(f"Making boot file system ({boot_fs})...")
#                     stdscr.refresh()
#
#                     # I think udev needs to notice the new partitions before running mkfs on them,
#                     # so I put a little timeout here.
#                     # Ok made a decorator out of this.
#                     # device_service.wait_for_partition(f"{device_service.get_device()}1")
#
#                     device_service.make_boot_fs()
#                     stdscr.addstr("Done\n")
#                     # device_service.read_boot_uuid()
#                     stdscr.addstr(f"Making root file system ({root_fs})...")
#                     stdscr.refresh()
#                     device_service.make_root_fs()
#                     stdscr.addstr("Done\n")
#                     stdscr.refresh()
#                     # device_service.read_root_uuid()
#                     if show_partitions(stdscr, device_service):
#                         stdscr.refresh()
#                         stdscr.addstr("\nPress any key to continue..")
#                         stdscr.getch()
#                         return 2
#                 return 0
#
#         stdscr.refresh()

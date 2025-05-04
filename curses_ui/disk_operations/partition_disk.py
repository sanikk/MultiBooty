from curses import KEY_ENTER, newwin, window
from curses_ui.common.controls import change_selection, check_quit_esc, close_window
from curses_ui.common.prints import (
    print_disk_entry,
    print_key_instructions,
    print_menu,
    print_top,
)
from curses_ui.common.prompts import selection_box, text_prompt
from disk_ops.device_service import DeviceService


def package_partition(stdscr: window, device_service: DeviceService):
    """
    Submenu to set package partition info.
    """
    selected = 0
    max_y, max_x = stdscr.getmaxyx()
    height, width = 8, 50
    win = newwin(height, width, max_y // 2 - height // 2, max_x // 2 - width // 2)
    while True:
        win.clear()
        win.box()
        win.addstr(1, 1, "Set package partition info")
        menu_items = [
            f"Make Package Partition: {device_service.get_package_partition()}",
            f"Package partition size: {device_service.get_package_partition_size()}",
            f"Package partition file system: {device_service.get_package_partition_fs()}",
        ]

        print_menu(win, menu_items, selected)

        key = stdscr.getch()
        if check_quit_esc(key):
            close_window(stdscr=stdscr, win=win)
            return 0
        selected = change_selection(key, selected, menu_items)
        if (key in (10, 13, KEY_ENTER) and selected == 0) or key == ord("1"):
            selection_box(
                stdscr=win,
                message=["Make a package partition?"],
                choices=[False, True],
                callback=device_service.set_package_partition,
                default_index=1,
            )
        if (key in (10, 13, KEY_ENTER) and selected == 1) or key == ord("2"):
            pass
        if (key in (10, 13, KEY_ENTER) and selected == 2) or key == ord("3"):
            selection_box(
                stdscr=win,
                message=["Pick a file system for the package partition"],
                choices=device_service.get_linux_fs_types(),
                callback=device_service.set_package_partition_fs,
                default_index=0,
            )
            pass


def partition_disk(stdscr: window, device_service: DeviceService, **kwargs):
    _ = kwargs

    boot_size = 100
    selected = 0
    stdscr.clear()
    stdscr.refresh()
    device_info = device_service.get_device_info()

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
            f"Set Package partition: {device_service.get_package_partition_info()}",
            f"Root partition size: rest of the disk",
            f"Root partition file system: {device_service.get_root_fs()}",
            f"Make hybrid MBR on disk: {device_service.get_hybrid_mbr()}",
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
                choices=device_service.get_fat_fs_types(),
                callback=device_service.set_boot_fs,
                default_index=0,
            )
        elif (key in (10, KEY_ENTER) and selected == 2) or key == ord("3"):
            package_partition(stdscr, device_service)

        elif (key in (10, KEY_ENTER) and selected == 4) or key == ord("5"):

            selection_box(
                stdscr=stdscr,
                message=["Please select a file system", "for the root partition."],
                choices=device_service.get_linux_fs_types(),
                callback=device_service.set_root_fs,
                default_index=0,
            )
        elif (key in (10, KEY_ENTER) and selected == 5) or key == ord("6"):
            selection_box(
                stdscr=stdscr,
                message=["Make a hybrid MBR to boot on legacy non-UEFI BIOS?"],
                choices=[True, False],
                callback=device_service.set_hybrid_mbr,
                default_index=0,
            )
        elif (key in (10, KEY_ENTER) and selected == 6) or key == ord("7"):
            device_service.partition_disk()

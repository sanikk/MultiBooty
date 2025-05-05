from curses import A_REVERSE, window
from disk_ops.device_service import DeviceService
from curses_ui.common.formatting import add_reverse, format_size


def print_key_instructions(
    stdscr: window, y_offset=0, y_start=None, numbers=True, updown=True
):
    instruction_text = f"{"Number" if numbers else ""}{" or " if numbers and updown else ""}{"Enter" if updown else ""} to select {"| ↑↓ or jk to move " if updown else ""}| esc to return | q to quit"
    max_y, x = stdscr.getmaxyx()
    if not y_start:
        y_start = max_y // 2 + y_offset
    x = x // 2 - len(instruction_text) // 2
    stdscr.addstr(y_start, x, instruction_text)
    stdscr.refresh()


def print_menu(
    stdscr: window, menu_items: list, selected: int, y_offset: int = 0, start_y=None
):
    h, w = stdscr.getmaxyx()
    if not start_y:
        start_y = h // 2 - len(menu_items) // 2 + y_offset

    for idx, item in enumerate(menu_items):
        y = start_y + idx
        item = f"{idx + 1}. {item}"
        x = w // 2 - len(item) // 2
        if idx == selected:
            add_reverse(stdscr, y, x, item)
        else:
            stdscr.addstr(y, x, item)

    stdscr.refresh()


def print_top(stdscr: window, device_service: DeviceService):
    """
    Draws the top box of each screen, with selected device.
    """
    ret = device_service.get_device_info()
    if ret:
        device, _, size, fstype, label, block_size = ret[0]
        stdscr.addstr(
            0,
            0,
            f"Device: {device:10}\nSize: {format_size(int(size)):10}\nFilesystem: {fstype}\nLabel: {label:10} Block size: {block_size:10}",
        )
    else:
        stdscr.addstr(0, 0, "No device selected.")
    stdscr.addstr(4, 0, "#" * (stdscr.getmaxyx()[1] - 1) + "\n")
    stdscr.refresh()


def print_device_node(win: window, device_node: tuple, i=None, selected=None):
    chosen = i is not None and selected is not None and i == selected
    if chosen:
        win.attron(A_REVERSE)
    win.addstr(
        f"{i + 1 if i is not None else "":3} {device_node[0]:10} {device_node[1]:10} {(int(device_node[1]) + int(device_node[2]) // int(device_node[5])) if device_node[1] else "":10} {int(device_node[2]) // int(device_node[5]):10} {format_size(int(device_node[2])):10}{device_node[3]:10} {device_node[4]:10}\n"
    )
    if chosen:
        win.attroff(A_REVERSE)


def print_disk_entry(stdscr: window, disk_entry, i=None):
    for device_node in disk_entry:
        if i is not None and device_node[1] == "":
            print_device_node(win=stdscr, device_node=device_node, i=i, selected=None)
        else:
            print_device_node(
                win=stdscr, device_node=device_node, i=None, selected=None
            )
        # stdscr.addstr(
        #     f"{i + 1 if i is not None and device_node[1] == '' else "":3} {device_node[0]:10} {device_node[1]:10} {(int(device_node[1]) + int(device_node[2]) // int(device_node[5])) if device_node[1] else "":10} {int(device_node[2]) // int(device_node[5]):10} {format_size(int(device_node[2])):10}{device_node[3]:10} {device_node[4]:10}\n"
        # )


def print_file_list(
    win: window, lst: list, showing: int, selected: int, y_offset=0, x_offset=0
):
    max_width = win.getmaxyx()[1] - 2
    linenumber = y_offset
    beginning = max(0, min(selected - showing // 2, len(lst) - showing))
    for idx, file_entry in lst[beginning : beginning + showing]:
        if idx == selected:
            add_reverse(win, linenumber, x_offset, f"{str(file_entry)[:max_width]}")

        else:
            win.addstr(linenumber, x_offset, f"{str(file_entry)[:max_width]}")
        linenumber += 1

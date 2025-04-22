from curses import A_REVERSE, window
from curses_ui.utils import format_size
from disk_ops.device_service import DeviceService


def print_key_instructions(stdscr: window):
    instruction_text = (
        "Number or Enter to select | ↑↓ or jk to move | esc to return | q to quit"
    )
    y = stdscr.getyx()[0]
    x = stdscr.getmaxyx()[1] // 2 - len(instruction_text) // 2
    stdscr.addstr(y + 2, x, instruction_text)
    stdscr.refresh()


def print_menu(stdscr: window, menu_items: list, selected: int, y_offset: int = 0):
    h, w = stdscr.getmaxyx()

    for idx, item in enumerate(menu_items):
        y = h // 2 - len(menu_items) // 2 + idx + y_offset
        item = f"{idx + 1}. {item}"
        x = w // 2 - len(item) // 2
        if idx == selected:
            stdscr.attron(A_REVERSE)
            stdscr.addstr(y, x, item)
            stdscr.attroff(A_REVERSE)
        else:
            stdscr.addstr(y, x, item)

    stdscr.refresh()


def print_top(stdscr: window, device_service: DeviceService):
    """
    Draws the top box of each screen, with selected device.
    """
    ret = device_service.get_device()
    if ret:
        device, _, size, fstype, label, block_size = ret
        stdscr.addstr(
            # f"{device_service.get_device()}"
            0,
            0,
            f"Device: {device:10}\nSize: {format_size(int(size)):10}\nFilesystem: {fstype}\nLabel: {label:10} Block size: {block_size:10}",
        )
    else:
        stdscr.addstr(0, 0, "No device selected.")
    stdscr.addstr(4, 0, "#" * (stdscr.getmaxyx()[1] - 1) + "\n")
    stdscr.refresh()


def print_disk_entry(stdscr: window, disk_entry, i: int):
    for device_node in disk_entry:
        stdscr.addstr(
            f"{i + 1 if not device_node[1] else "":3} {device_node[0]:10} {device_node[1]:10} {(int(device_node[1]) + int(device_node[2]) // int(device_node[5])) if device_node[1] else "":10} {int(device_node[2]) // int(device_node[5]):10} {format_size(int(device_node[2])):10}{device_node[3]:10} {device_node[4]:10}\n"
        )

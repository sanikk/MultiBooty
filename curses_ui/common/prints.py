from curses import A_REVERSE, window
import curses
import sys


def print_key_instructions(stdscr: window):
    instruction_text = (
        "Number or Enter to select | ↑↓ or jk to move | esc to return | q to quit"
    )
    y = stdscr.getyx()[0]
    x = stdscr.getmaxyx()[1] // 2 - len(instruction_text) // 2
    # stdscr.addstr("Number or Enter to select | ↑↓ or jk to move | q to quit")
    stdscr.addstr(y + 2, x, instruction_text)
    stdscr.refresh()


def print_menu(stdscr, menu_items, selected, y_offset=0):
    h, w = stdscr.getmaxyx()

    for idx, (item, _) in enumerate(menu_items):
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


def print_top(stdscr: window, device_service):
    """
    Draws the top box of each screen, with selected device.
    """
    stdscr.addstr(0, 0, f"Device: {device_service.get_device()}")
    stdscr.addstr(1, 0, "#" * (stdscr.getmaxyx()[1] - 1) + "\n")
    stdscr.refresh()

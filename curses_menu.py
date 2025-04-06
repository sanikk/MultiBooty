import curses
from curses_ui.new_partitions import new_partitions_screen
from curses_ui.select_block_device import select_block_device_screen
from curses_ui.show_device_info import show_device_info_screen
from curses_ui.install_grub import install_grub_screen
from curses_ui.configure_grub import configure_grub_screen

menu_items = [
    ("Select device", select_block_device_screen),
    ("Device info", show_device_info_screen),
    ("New partitions", new_partitions_screen),
    ("Install GRUB", install_grub_screen),
    ("Configure GRUB", configure_grub_screen),
]


def main_menu(stdscr):
    curses.curs_set(0)  # Hide cursor
    selected = 0
    device = None

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for idx, (item, func) in enumerate(menu_items):
            x = w // 2 - len(item) // 2
            y = h // 2 - len(menu_items) // 2 + idx
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item)

        stdscr.refresh()

        key = stdscr.getch()
        if key in [curses.KEY_UP, ord("k")]:
            selected = (selected - 1) % len(menu_items)
        elif key in [curses.KEY_DOWN, ord("j")]:
            selected = (selected + 1) % len(menu_items)
        elif key in [curses.KEY_ENTER, 10, 13]:
            selected, args = menu_items[selected][1](stdscr=stdscr, device=device)
            # return selected  # or call function for that step here
        elif key in [27, ord("q")]:  # Esc or q
            break


if __name__ == "__main__":
    curses.wrapper(main_menu)

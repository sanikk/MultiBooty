import curses
from grub.grub_runners import make_grub


def install_grub_screen(stdscr, dev):
    # TODO: ok this needs an update to a menu based screen. options have defaults, scroll through them, change as needed.
    stdscr.clear()

    mountpoint = "/mnt"
    arch = True
    legacy = True

    stdscr.addstr("Install grub\n\n")

    stdscr.addstr(f"Enter mountpoint [{mountpoint}]: ")
    stdscr.refresh()
    curses.echo()
    user_input = stdscr.getstr().decode().strip()
    if user_input:
        mountpoint = user_input
    curses.noecho()

    stdscr.addstr("Use x64 architecture? (y/n) [y]: ")
    stdscr.refresh()
    curses.echo()
    arch_input = stdscr.getstr().decode().strip().lower()
    if arch_input == "n":
        arch = False
    curses.noecho()

    partition = f"{dev}1"

    stdscr.addstr(f"\nRunning grub-install on {partition}...\n")
    stdscr.refresh()

    make_grub(partition=partition, mountpoint=mountpoint, x64=arch)

    stdscr.addstr("Done.\n")
    stdscr.refresh()

    stdscr.addstr("\\nPress any key to continue...")
    stdscr.refresh()
    stdscr.getch()
    return (None,)

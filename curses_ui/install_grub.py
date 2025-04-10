import curses
from pathlib import Path
from curses_ui.prompts import text_prompt
from grub.grub_runners import make_grub


def old_install_grub_screen(stdscr, dev):
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


def install_grub_screen(stdscr, device_service, grub_service):
    curses.curs_set(1)
    mountpoint = "/mnt"
    arch = "amd64"
    selected = 2  # default to "Install GRUB"

    def draw():
        stdscr.clear()
        stdscr.addstr(0, 0, "GRUB Installation", curses.A_BOLD | curses.A_UNDERLINE)

        options = [
            f"Mountpoint: {mountpoint}",
            f"Architecture: {arch}",
            "Install GRUB",
        ]

        for idx, label in enumerate(options):
            attr = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            stdscr.addstr(2 + idx, 2, label, attr)

        stdscr.addstr(6, 0, "↑↓ or jk to move | Enter to edit/run | q to quit")
        stdscr.refresh()

    while True:
        draw()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % 3
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % 3
        elif key == ord("q"):
            break
        elif key in (10, 13):  # Enter
            if selected == 0:
                ret = text_prompt(stdscr, len("Mountpoint: "))
                if ret and Path(ret).exists() and Path(ret).is_dir():
                    grub_service.set_mountpoint(ret)
            elif selected == 1:
                selection_box(
                    stdscr,
                    "Select an architecture",
                    ["amd64", "i386", "arm"],
                    ["amd64", "i386", "arm"].index(arch),
                    lambda val: (
                        grub_service.set_arch(val),
                        globals().__setitem__("arch", val),
                    ),
                )
            elif selected == 2:
                grub_service.install_grub()
                return 3
                break

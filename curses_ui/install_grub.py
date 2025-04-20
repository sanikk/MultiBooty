import curses
from pathlib import Path
from sys import exit
from curses_ui.prompts import text_prompt, selection_box
from curses_ui.utils import print_key_instructions


def install_grub_screen(stdscr, grub_service, **kwargs) -> int:
    """
    Screen that let's user run grub-install on the device.

    Args:
        stdscr: screen
        grub_service(GrubService): grub service instance to use.
    Returns:
        next_screen(int): the index of the next screen to use as default.
    """
    _ = kwargs

    mountpoint = "/mnt"
    arch = "amd64"
    selected = 2

    while True:
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

        print_key_instructions(stdscr)

        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % 3
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % 3
        elif key == ord("q"):
            exit(0)
        elif key in (10, 13):
            if selected == 0:
                ret = text_prompt(stdscr, 2, len("Mountpoint: "))
                if ret and Path(ret).exists() and Path(ret).is_dir():
                    grub_service.set_mountpoint(ret)
            elif selected == 1:
                selection_box(
                    stdscr,
                    "Select an architecture",
                    ["amd64", "i386", "arm"],
                    grub_service.set_arch,
                    0,
                )

            elif selected == 2:
                stdscr.addstr("Installing grub...")
                stdscr.refresh()
                grub_service.install_grub()
                stdscr.addstr("Done")
                return 3

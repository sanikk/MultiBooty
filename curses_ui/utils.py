def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def handle_return_value(stdscr, ret):
    if ret.success:
        stdscr.addstr("Done! No errors.")
        return True
    for error in ret.errors:
        stdscr.addstr(error)
    return False


def print_lines(stdscr, lines):
    for line in lines:
        stdscr.addstr(line + "\n")

import subprocess, shlex


def parse_lsblk_output(output: str):
    parsed = []
    for line in output.strip().splitlines():
        parsed.append(tuple(a.split("=")[1] for a in shlex.split(line)))
    return parsed


def disk_info(device: str) -> list:
    """
    Reads and parses the lsblk info for the given device.
    Used in select_device,

    Args
        device (str): device to read

    Return
        list - a list of tuples with path, start, size, fstype, label
    """
    ret = subprocess.run(
        ["lsblk", "-b", "-P", "-o", "PATH,START,SIZE,FSTYPE,LABEL,PHY-SEC", device],
        text=True,
        capture_output=True,
    )
    if ret and ret.returncode == 0:
        parsed = []
        for line in ret.stdout.strip().split("\n"):
            parsed.append(tuple(a.split("=")[1] for a in shlex.split(line)))
        return parsed

    return ret.stderr.strip().split("\n")

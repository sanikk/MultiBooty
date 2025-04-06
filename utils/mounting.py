from pathlib import Path
from utils.runners import run_subprocess_with_sudo

from subprocess import run


def is_mounted(mountpoint):
    with open("/proc/mounts") as f:
        return any(line.split()[1] == mountpoint for line in f)


def mount_command(dev, mountpoint):
    run_subprocess_with_sudo("mount", [dev, mountpoint])


def unmount_command(dev):
    run_subprocess_with_sudo("umount", [dev])


def mounted(func):
    def wrapper(partition, mountpoint, *args, **kwargs):
        if is_mounted(mountpoint):
            return False, f"{mountpoint} was not empty."
        mount_command(partition, mountpoint)
        try:
            if not is_mounted(mountpoint):
                return False, f"Mounting {partition} on {mountpoint} failed."
            return func(partition, mountpoint, *args, **kwargs)
        finally:
            unmount_command(partition)

    return wrapper

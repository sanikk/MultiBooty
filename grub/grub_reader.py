from sys import argv, stderr
from utils.mounting import mounted
from pathlib import Path


@mounted
def file_reader(partition, mountpoint="/mnt"):
    """
    File reader function made to read grub.cfg from the boot partition.
    I might reuse this so I keep it general.
    Because of the mounting this requires SUDO to run.

    Args
        partition (str): boot partition device node. Used by the mounted decorator.
        mountpoint (str): where to mount the partition on the local file system. Used by the mounted decorator too.
    """
    try:
        grubconfig = Path(mountpoint, "boot", "grub", "grub.cfg")
        with open(grubconfig) as f:
            return f.read()
    except Exception as e:
        print(f"Error in grub/file_reader:", file=stderr)
        print(e, file=stderr)


if __name__ == "__main__":
    """
    Because of the mounted decorator the function requires the mountpoint parameter.
    """
    if len(argv) == 3:

        print(file_reader(argv[1], argv[2]))

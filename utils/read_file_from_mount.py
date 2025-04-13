from sys import argv, stderr
from utils.mounting import mounted
from pathlib import Path


@mounted
def read_mounted_file(partition, mountpoint, path, filename):
    """
    File reader function made to read grub.cfg from the boot partition.
    I might reuse this so I keep it general.
    Because of the mounting this requires SUDO to run.

    Args
        partition (str): boot partition device node. Used by the mounted decorator.
        mountpoint (str): where to mount the partition on the local file system. Used by the mounted decorator.
        path (str): path to file inside the partition/mountpoint
        filename (str): name of the file to read
    """
    try:
        filepath = Path(mountpoint, path, filename)
        with open(filepath) as f:
            return f.read()
    except Exception as e:
        print(f"Error in utils/read_mounted_file:", file=stderr)
        print(e, file=stderr)


if __name__ == "__main__":
    """
    Because of the @mounted decorator the function requires the partition and mountpoint parameters.

    Args:
        partition (str): partition the file is on
        mountpoint (str): where to mount the partition for the file read
        path (str): path to file inside the partition/mountpoint
        filename (str): name of the file to read

    Return
        file contents in stdout
    """
    if len(argv) == 4:
        print(read_mounted_file(*argv[1:]))
        exit(0)
    exit(1)

# from utils.mounting import mounted
from sys import exit, argv
from pathlib import Path


def make_root_folders(partition: str, mountpoint: str):
    """
    Makes folders on the root partition.
    Decorator needs partition and mountpoint.

    """
    _ = partition

    for dir in ["isos", "MultiBooty", "packages"]:
        Path(mountpoint, dir).mkdir()
    for dir in ["arch_linux", "debian"]:
        Path(mountpoint, "packages", dir).mkdir()


if __name__ == "__main__":
    if len(argv) == 3:
        make_root_folders(argv[1], argv[2])
        exit(0)
    exit(1)

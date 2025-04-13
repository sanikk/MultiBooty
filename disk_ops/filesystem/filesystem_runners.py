from utils.mounting import mounted
from utils.runners import run_subprocess_with_sudo
from pathlib import Path


def make_fat32_filesystem(dev, partition):
    """
    Make FAT32 filesystem.
    """
    ret = run_subprocess_with_sudo("mkfs.fat", ["-F32", f"{dev}{partition}"])

    if ret.returncode == 0:
        return True
    return False


def make_ext4_filesystem(dev, partition):
    """
    Make ext4 filesystem with no journaling.
    """
    ret = run_subprocess_with_sudo(
        "mkfs.ext4", ["-O", "^has_journal", f"{dev}{partition}"]
    )

    if ret.returncode == 0:
        return True
    return False


def label_root(partition: str, label: str = "MultiBootyRoot"):
    """
    Sets root partition label.
    This is used on some grub configs.
    """
    ret = run_subprocess_with_sudo("e2label", [partition, label])
    if ret.returncode == 0:
        return True
    return False


@mounted
def make_root_folders(partition, mountpoint):
    for dir in ["isos", "MultiBooty", "packages"]:
        Path(mountpoint, dir).mkdir()
    for dir in ["arch_linux", "debian"]:
        Path(mountpoint, "packages", dir).mkdir()

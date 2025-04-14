from disk_ops.disks.disk_runners import wait_for_device_node
from utils.mounting import mounted, partition_unmounted
from utils.runners import run_subprocess_with_sudo
from pathlib import Path
from subprocess import run


# @partition_unmounted
@wait_for_device_node
def make_fat32_filesystem(partition):
    """
    Make FAT32 filesystem.
    Decorator needs partition.
    """
    ret = run_subprocess_with_sudo("mkfs.fat", ["-F32", f"{partition}"])

    if ret.returncode == 0:
        return True
    return False


# @partition_unmounted
@wait_for_device_node
def make_ext4_filesystem(partition):
    """
    Make ext4 filesystem with no journaling.
    Decorator needs partition.
    """
    ret = run_subprocess_with_sudo("mkfs.ext4", ["-O", "^has_journal", f"{partition}"])
    if ret.returncode == 0:
        return True
    return False


@partition_unmounted
@wait_for_device_node
def label_root(partition: str, label: str = "MultiBootyRoot"):
    """
    Sets root partition label.
    This is used on some grub configs.
    Decorator needs partition.
    """
    ret = run_subprocess_with_sudo("e2label", [partition, label])
    if ret.returncode == 0:
        return True
    return False


@mounted
def make_root_folders(partition, mountpoint):
    """
    Makes folders on the root partition.
    Decorator needs partition.

    """
    _ = partition

    for dir in ["isos", "MultiBooty", "packages"]:
        Path(mountpoint, dir).mkdir()
    for dir in ["arch_linux", "debian"]:
        Path(mountpoint, "packages", dir).mkdir()


@wait_for_device_node
def read_partition_uuid(partition):
    ret = run(["blkid", "-s", "UUID", "-o", "value", partition])
    if ret and ret.returncode == 0:
        return ret.stdout

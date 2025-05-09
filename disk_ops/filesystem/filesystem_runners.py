from curses import endwin
from disk_ops.disks.disk_runners import wait_for_device_node
from utils.mounting import mounted, partition_unmounted
from utils.runners import run_python_subprocess_with_sudo, run_subprocess_with_sudo


@partition_unmounted
@wait_for_device_node
def make_fat32_filesystem(partition):
    """
    Make FAT32 filesystem.
    Decorator needs partition.
    """
    ret = run_subprocess_with_sudo("mkfs.fat", ["-F32", "-n", "MULTIBBOOT", partition])

    if ret and ret.returncode == 0:
        return True
    # TODO: add proper error handling
    endwin()
    print(ret.stderr)
    return False


@partition_unmounted
@wait_for_device_node
def make_fat16_filesystem(partition):
    # TODO: ok this can only handle 2gb partitions. maybe add a help entry for that?
    ret = run_subprocess_with_sudo("mkfs.fat", ["-F16", "-n", "MULTIBBOOT", partition])
    if ret and ret.returncode == 0:
        return True
    # TODO: add proper error handling
    endwin()
    print(ret.stderr)
    return False


@partition_unmounted
@wait_for_device_node
def make_ext4_filesystem(partition):
    """
    Make ext4 filesystem with no journaling.
    Decorator needs partition.
    """
    ret = run_subprocess_with_sudo(
        "mkfs.ext4", ["-O", "^has_journal", "-L", "MultiBootyRoot", partition]
    )
    if ret.returncode == 0:
        return True
    return False


def make_ext2_filesystem(partition):
    ret = run_subprocess_with_sudo("mkfs.ext2", ["-L", "MultiBootyRoot", partition])
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
@wait_for_device_node
def make_root_folders(partition, mountpoint):
    ret = run_python_subprocess_with_sudo(
        "disk_ops/filesystem/make_root_folders.py", [partition, mountpoint]
    )
    print(ret)
    if ret and ret.returncode == 0:
        return True

    return False


@wait_for_device_node
def read_partition_uuid(partition):
    """
    Reads UUID of partition.
    Decorator needs partition.
    """
    ret = run_subprocess_with_sudo("blkid", ["-s", "UUID", "-o", "value", partition])
    if ret and ret.returncode == 0:
        return ret.stdout.strip()

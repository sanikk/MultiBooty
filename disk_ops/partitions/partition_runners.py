from utils.runners import run_python_subprocess_with_sudo
import json

# from parted import IOException


def propose_partitions(device: str, size_in_mb: int) -> dict:
    """
    SUDO
    Figures out an aligned layout for a disk, given boot partition size.
    Does not write to disk. Dry-run.

    Args:
        device (str): device to dry-partition, "/dev/sdc"
        size_in_mb(int): size of boot partition

    Returns:
        dict
    """
    try:
        ret = run_python_subprocess_with_sudo(
            "disk_ops/partitions/propose_partitions.py",
            [device, str(size_in_mb)],
        )
        if ret:
            if ret.returncode == 0:
                device_infos = json.loads(ret.stdout)
                return device_infos
            return {"error": ret.stderr}
    except Exception as e:
        print(f"Invalid device node {device}.")
        return {"error": f"invalid device node {device}"}
    return {"error": "No return value"}


def make_partitions(
    device: str,
    boot_start: int,
    boot_end: int,
    root_start: int,
    root_end: int,
    # table_type="gpt", optimum=True
) -> tuple[bool, str]:
    """
    SUDO
    Actually writes the partitions to disk.

    Args:
        device (str): device_node, "/dev/sdc"
        boot_start (int): start sector of boot partition
        boot_end (int): end sector of boot partition
        root_start (int): start sector of ext4 root partition
        root_end (int): end sector of root partition
    Not implemented yet:
        table_type (bool?): gpt or mbr

    Returns:
        bool: True for success
    """
    try:
        ret = run_python_subprocess_with_sudo(
            "disk_ops/partitions/partition_disk.py",
            [
                device,
                str(boot_start),
                str(boot_end),
                str(root_start),
                str(root_end),
                # table_type, optimum
            ],
        )
        if ret:
            if ret.returncode == 0:
                return (
                    True,
                    f"Wrote boot {boot_start}-{boot_end} and root {root_start}-{root_end} to {device}.",
                )
            return False, ret.stderr
    except Exception as e:
        return False, f"Invalid device node {device}."

    return False, "Something went wrong."

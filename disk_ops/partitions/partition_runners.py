from disk_ops.runners import run_python_subprocess_with_sudo
import json
from parted import IOException


def propose_partitions(dev: str, size_in_mb: int):
    ret = run_python_subprocess_with_sudo(
        "disk_ops/propose_partitions.py",
        [dev, str(size_in_mb)],
        IOException,
        f"Invalid device node {dev}.",
    )
    if ret:
        if ret.returncode == 0:
            device_infos = json.loads(ret.stdout)
            return device_infos
        return {"error": ret.stderr}
    return {"error": "No return value"}


def make_partitions(
    dev: str,
    boot_start: int,
    boot_end: int,
    root_start: int,
    root_end: int,
    # table_type="gpt", optimum=True
):
    ret = run_python_subprocess_with_sudo(
        "disk_ops/partition_disk.py",
        [
            dev,
            str(boot_start),
            str(boot_end),
            str(root_start),
            str(root_end),
            # table_type, optimum
        ],
        IOException,
        f"Invalid device node {dev}.",
    )

    if ret:
        return ret.stdout
        # if ret.returncode == 0:

    return ""

from utils.runners import run_python_subprocess_with_sudo


def wait_for_device_node(func):
    def wrapper(partition, **kwargs):
        ret = run_python_subprocess_with_sudo(
            "disk_ops/disks/wait_for_device_node.py", [partition]
        )
        if ret and ret.returncode == 0:
            return func(partition=partition, **kwargs)
        raise RuntimeError(f"Timeout waiting for {partition}")

    return wrapper

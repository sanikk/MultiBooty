from disk_ops.runners import run_subprocess_with_sudo
import json


def get_disk_info(devs):
    print("We need sudo to collect device info.")
    print("This is a read-only op.")
    ret = run_subprocess_with_sudo(
        "disk_ops/disk_info_linux.py", devs, FileNotFoundError, "No such device."
    )
    if ret and ret.returncode == 0:
        device_infos = json.loads(ret.stdout)
        return device_infos
    else:
        if not ret:
            print("Error: no return value from gathering device info")
        else:
            print("Error:", ret.stderr)
        return None

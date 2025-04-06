from utils.runners import run_python_subprocess_with_sudo
import json


def get_disk_info(devs: list[str]) -> dict:
    """
    SUDO
    Collects info on number of sectors, their size and total device size.

    Args:
        dev (list[str]): list of devices to collect data on, ["/dev/sda", "/dev/sdb"]

    Returns:
        dict:   {"sector_size": sector_size,
                "num_sectors": num_sectors,
                "size_bytes": size_bytes,}
    """
    # TODO: move this printing to it's own function that we inject here if using text UI.
    # TODO: make one like this for GUI too, and inject it here if using GUI.
    print("We need sudo to collect device info.")
    print("We'll be reading sector size and size in bytes")
    print(f"from devices: {devs}.")
    print("This is a read-only op.")
    ret = run_python_subprocess_with_sudo("disk_ops/disks/disk_info_linux.py", devs)
    if ret and ret.returncode == 0:
        device_infos = json.loads(ret.stdout)
        return device_infos
    else:
        if not ret:
            print("Error: no return value from gathering device info")
        else:
            print("Error:", ret.stderr)
            if not ret.stderr:
                print("No devices found")
        return {}

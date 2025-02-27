from runners import run_subprocess_with_sudo
import json


def gather_device_info(devs):
    print("We need sudo to collect device info with PyParted.")
    print("This is a read-only op.")
    ret = run_subprocess_with_sudo(
        "disk_ops/partition_info.py",
        devs,
        ModuleNotFoundError,
        "Module PyParted not found. We should probably be running in a virtual environment with pyparted installed.",
    )
    if ret and ret.returncode == 0:
        device_infos = json.loads(ret.stdout)
        return {
            dev["device"]: {
                "hybrid_iso": dev["hybrid_iso"],
                "free_space": dev["free_space"],
                "partitions": dev["partitions"],
            }
            for dev in device_infos
        }
    else:
        if not ret:
            print("Error: no return value from gathering device info")
        else:
            print("Error:", ret.stderr)
        return None


if __name__ == "__main__":
    print(gather_device_info(["/dev/sdc"]))

import subprocess, sys, json

from parted import IOException


vpython = ""
try:
    vpython = subprocess.run(
        ["which", "python3"], capture_output=True, text=True
    ).stdout.strip()
except Exception as e:
    print("Something went wrong trying to find a python3 with which.")
    print(e)
if not vpython:
    print("No local python3 found. Exiting with extreme prejudice.")
    sys.exit(1)


def run_python_subprocess_with_sudo(
    command, arguments: list, error_type, error_message: str
):
    try:
        return subprocess.run(
            ["sudo", vpython, command, *arguments],
            capture_output=True,
            text=True,
        )
    except error_type:
        print(f"{error_type}: {error_message}", file=sys.stderr)
        return None


def run_subprocess_with_sudo(command, arguments: list, error_type, error_message: str):
    try:
        return subprocess.run(
            ["sudo", command, *arguments], capture_output=True, text=True, check=True
        )
    except error_type:
        print(f"{error_type}: {error_message}", file=sys.stderr)
        return None


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

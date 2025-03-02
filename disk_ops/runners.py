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


def run_subprocess_with_sudo(command, arguments: list, error_type, error_message: str):
    try:
        return subprocess.run(
            ["sudo", vpython, command, *arguments],
            capture_output=True,
            text=True,
        )
    except error_type:
        print(f"{error_type}: {error_message}", file=sys.stderr)
        return None


def propose_partitions(dev: str, size_in_mb: int):
    ret = run_subprocess_with_sudo(
        "disk_ops/proposed_partitioning.py",
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

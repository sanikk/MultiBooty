import subprocess, sys


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
        print(error_message)
        return None

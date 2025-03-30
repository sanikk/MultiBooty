import subprocess, sys, json


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


def run_python_subprocess_with_sudo(command, arguments: list):
    """
    Run a python script in a subprocess with elevated priviledges.
    Should use the python of possible virtual env.

    Args:
        command (str): the actual command to run, "ls"
        arguments (list[str]): list of arguments for the command

    Returns:
        subprocess return value
    """
    # TODO: add check to see if we even need sudo
    return subprocess.run(
        ["sudo", vpython, command, *arguments],
        capture_output=True,
        text=True,
    )


def run_subprocess_with_sudo(command, arguments: list):
    """
    Run a program in a subprocess with elevated priviledges.

    Args:
        command (str): the actual command to run, "ls"
        arguments (list[str]): list of arguments for the command

    Returns:
        subprocess return value
    """
    # TODO: add check to see if we even need sudo
    return subprocess.run(
        ["sudo", command, *arguments], capture_output=True, text=True, check=True
    )

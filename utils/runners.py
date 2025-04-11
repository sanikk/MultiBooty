from subprocess import run
from sys import exit
from os import geteuid


vpython = ""
try:
    vpython = run(["which", "python3"], capture_output=True, text=True).stdout.strip()
except Exception as e:
    print("Something went wrong trying to find a python3 with which.")
    print(e)
if not vpython:
    print("No local python3 found. Exiting with extreme prejudice.")
    exit(1)


def run_python_subprocess_with_sudo(command, arguments: list):
    """
    Run a python script in a subprocess, with elevated priviledges if needed.
    Should use the python of possible virtual env.

    Args:
        command (str): the actual command to run, "ls"
        arguments (list[str]): list of arguments for the command

    Returns:
        subprocess return value
    """
    if geteuid() == 0:
        return run(
            [vpython, command, *arguments],
            capture_output=True,
            text=True,
        )
    return run(
        ["sudo", vpython, command, *arguments],
        capture_output=True,
        text=True,
    )


def run_subprocess_with_sudo(command, arguments: list):
    """
    Run a program in a subprocess, with elevated priviledges if needed.

    Args:
        command (str): the actual command to run, "ls"
        arguments (list[str]): list of arguments for the command

    Returns:
        subprocess return value
    """
    if geteuid() == 0:
        return run([command, *arguments], capture_output=True, text=True, check=True)
    return run(
        ["sudo", command, *arguments], capture_output=True, text=True, check=True
    )

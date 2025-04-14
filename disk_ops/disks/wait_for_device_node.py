from sys import argv
from os import path
from time import sleep


def wait_for_device_node(device_node):
    """
    Function that waits until the device_node is available,
    or times out.

    Args
        device_node (str): device node to wait for, for example "/dev/sdc1"

    Return returncode
        0 - success, device is available now
        1 - fail, wrong arguments
        2 - fail, timed out
    """
    for _ in range(100):
        if path.exists(device_node):
            try:
                with open(device_node, "rb"):
                    exit(0)
            except OSError:
                pass  # Exists but not ready yet
        sleep(0.1)
    exit(2)


if __name__ == "__main__":
    if len(argv) == 2:
        wait_for_device_node(argv[1])
    print(f"error with args: {argv}")
    exit(1)

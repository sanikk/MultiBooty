from ast import arguments
import re
from subprocess import CalledProcessError
from utils.runners import run_subprocess_with_sudo


def make_new_gpt(device):
    try:
        ret = run_subprocess_with_sudo(command="sgdisk", arguments=["-Z", "-o", device])
        if ret and ret.returncode == 0:
            # print(ret.stdout)
            return True
        if ret:
            print(ret.stderr)
    except CalledProcessError as e:
        print(e)
        print(e.stderr)
    return False


def read_usable_sectors(device: str) -> tuple | None:
    ret = run_subprocess_with_sudo(command="sgdisk", arguments=["--print", device])
    if ret and ret.returncode == 0:
        pattern = r"First usable sector is (\d+), last usable sector is (\d+)"
        result = re.search(pattern, ret.stdout)
        if result and result.group(1) and result.group(2):
            return result.group(1, 2)
    return None


def make_partition(device, partnum=0, start: int | str = 0, end: int | str = 0):
    """
    Makes new GPT partition with sgdisk.
    Default values pick
    - first available partition number
    - start of biggest available block, exluding gpt table
    - end of biggest available block, exluding backup gpt table
    """
    ret = run_subprocess_with_sudo(
        command="sgdisk", arguments=[f"--new={partnum}:{start}:{end}", device]
    )
    if ret and ret.returncode == 0:
        return True
    return False


def make_next_partition(device, size=None, esp: bool = False):
    """
    Makes new GPT partition with sgdisk.
    Default values pick
    - first available partition number
    - start of biggest available block, exluding gpt table
    - end of biggest available block, exluding backup gpt table
    """
    ret = run_subprocess_with_sudo(
        command="sgdisk",
        arguments=[f"--new=0:0:{'+'+str(size)+"MB" if size else '0'}", device],
    )
    if ret and ret.returncode == 0:
        # if esp:
        #     ret = run_subprocess_with_sudo(
        #         command="sgdisk", arguments=["--typecode=1:ef00", device]
        #     )
        # else:
        #     ret = run_subprocess_with_sudo(
        #         command="sgdisk", arguments=["--typecode=2:8300", device]
        #     )
        if ret and ret.returncode == 0:
            return True
    return False


def make_protective_mbr(device, package_partition: bool):

    ret = run_subprocess_with_sudo(
        command="sgdisk", arguments=["--typecode=1:ef00", device]
    )
    if ret and ret.returncode == 0:
        print("0 succesful")

        ret = run_subprocess_with_sudo(
            command="sgdisk", arguments=["--typecode=2:8300", device]
        )
        if ret and ret.returncode == 0:
            print("1 succesful")
            if package_partition:
                ret = run_subprocess_with_sudo(
                    command="sgdisk", arguments=["--typecode=3:8300", device]
                )
                if ret and ret.returncode == 0:
                    print("made 3rd partition")
                    ret = run_subprocess_with_sudo(
                        command="sgdisk",
                        arguments=["--hybrid=1:2:3", "--attributes=1:set:2", device],
                    )
                    if ret and ret.returncode == 0:
                        return True
            else:
                ret = run_subprocess_with_sudo(
                    command="sgdisk", arguments=["--hybrid=1:2", device]
                )
                if ret and ret.returncode == 0:
                    return True
    if ret:
        print(ret.stderr)
    return False


def verify_gpt(device) -> tuple[bool, list]:
    """
    Function that uses sgdisk to verify a GPT table.

    Args
        device (str): the device_node to verify.

    Return
        bool - op was succesful
        list - list of warnings

    """
    ret = run_subprocess_with_sudo(command="sgdisk", arguments=["-v", device])
    if ret and ret.returncode == 0:
        if "No problems found" in ret.stdout:
            cautions = re.findall(r"Caution:.*?(?:\n(?!\n).*)*\n\n", ret.stdout)
            return True, cautions
    return False, [ret.stdout, ret.stderr]


def print_partitions(device):
    """
    Used for debugging.

    """
    ret = run_subprocess_with_sudo("sgdisk", ["--print", device])

    print(ret.stdout)


# def make_some_mbr_thing(device):
#     pass
# sgdisk -t 3:ef02 /dev/sdb
# sudo grub-install --boot-directory=/mnt/boot --force --target=i386-pc /dev/sdb   -v

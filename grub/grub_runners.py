from utils.runners import run_subprocess_with_sudo, run_python_subprocess_with_sudo
from utils.mounting import mounted


architectures = {
    "amd64": "x86_64-efi",
    "i386": "i386-efi",
    # "arm"
}


@mounted
def make_grub(partition: str, mountpoint: str, architecture: str) -> bool:
    """
    Does grub-install on a given partition.

    Args:
        partition (str): Partition where to install grub "/dev/sdc1"
        mountpoint (str): Where to mount partition for the operation "/mnt"

    Returns:
        bool: True for success
    """
    if (
        not partition
        or not mountpoint
        or not architecture
        or architecture not in architectures
    ):
        return False
    try:
        ret = run_subprocess_with_sudo(
            "grub-install",
            [
                "--removable",
                "--no-nvram",
                f"--target={architectures[architecture]}",
                f"--efi-directory={mountpoint}",
                "--bootloader-id=GRUB",
                f"--boot-directory={mountpoint}/boot",
            ],
        )
        if ret:
            return ret.returncode == 0
    except Exception as e:
        print(f"Error running grub-install: {e}")
    return False


def read_grub_file(device):
    ret = run_python_subprocess_with_sudo("grub/grub_reader.py", [f"{device}1"])
    return ret

from utils.runners import run_subprocess_with_sudo
from utils.mounting import mounted

architectures = {
    "amd64": "x86_64-efi",
    "i386": "i386-efi",
    # "arm"
}


@mounted
# def make_grub(partition: str, mountpoint: str, x64: bool = True):
def make_grub(partition: str, mountpoint: str, architecture: str):
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
        return
    try:
        ret = run_subprocess_with_sudo(
            "grub-install",
            [
                # "--removable",
                # "--target=x86_64-efi",
                f"--target={architectures[architecture]}",
                f"--efi-directory={mountpoint}",
                "--bootloader-id=GRUB",
                f"--boot-directory={mountpoint}/boot",
            ],
        )
        # umount = umount_partition(dev, 1)
        return ret
        if ret:
            return ret.returncode == 1
    except Exception as e:
        print(f"Error running grub-install: {e}")
    return False

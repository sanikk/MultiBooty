from utils.runners import run_subprocess_with_sudo
from utils.mounting import mounted


@mounted
def make_grub(partition: str, mountpoint: str, x64: bool = True):
    """
    Does grub-install on a given partition.

    Args:
        partition (str): Partition where to install grub "/dev/sdc1"
        mountpoint (str): Where to mount partition for the operation "/mnt"

    Returns:
        bool: True for success
    """
    target = "x86_64-efi"
    if not x64:
        target = "i386-efi"
    try:
        ret = run_subprocess_with_sudo(
            "grub-install",
            [
                # "--removable",
                # "--target=x86_64-efi",
                f"--target={target}",
                f"--efi-directory={mountpoint}",
                "--bootloader-id=GRUB",
                f"--boot-directory={mountpoint}/boot",
            ],
            ValueError,
            "glub",
        )
        # umount = umount_partition(dev, 1)
        return ret
        if ret:
            return ret.returncode == 1
    except Exception as e:
        print(f"Error running grub-install: {e}")
    return False

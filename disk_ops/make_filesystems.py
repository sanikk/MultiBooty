from disk_ops.runners import run_subprocess_with_sudo


def make_boot_filesystem(dev, partition):
    """
    Make FAT32 filesystem.
    """
    run_subprocess_with_sudo(
        "mkfs.fat", ["-F32", f"{dev}{partition}"], ValueError, "bleb"
    )
    # subprocess.run(["mkfs.fat", "-F32", f"{dev}{partition}"], check=True)


def make_ext_filesystem(dev, partition):
    """
    Make ext4 filesystem with no journaling.
    """
    run_subprocess_with_sudo(
        "mkfs.ext4", ["-O", "^has_journal", f"{dev}{partition}"], ValueError, "blob"
    )
    # subprocess.run(["mkfs.ext4", "-O", "^has_journal", f"{dev}{partition}"], check=True)

import subprocess, json


def translate_partition_type(code):
    """
    Translates a partition type code to a name.
    """
    PARTITION_TYPES = {
        "0x00": "Empty",
        "0x01": "FAT12",
        "0x04": "FAT16 <32M",
        "0x05": "Extended",
        "0x06": "FAT16",
        "0x07": "NTFS",
        "0x0b": "FAT32",
        "0x0c": "FAT32 LBA",
        "0x0e": "FAT16 LBA",
        "0x0f": "Extended LBA",
        "0x82": "Linux swap",
        "0x83": "Linux",
        "0x8e": "Linux LVM",
        "0xef": "EFI System",
        "0xfd": "Linux RAID",
    }
    return PARTITION_TYPES.get(code, "Unknown Partition Type")


def gather_block_info(dev):
    """
    USERSPACE
    Gathers info about a single block device.

    Args:
        dev (str): Block device to inspect.

    Returns:
        dict: The lsblk output for the device or an empty dict.
    """
    ret = subprocess.run(
        [
            "lsblk",
            "-J",
            "-o",
            "NAME,PHY-SeC,LOG-Sec,SIZE,label,model,vendor,fstype,PARTTYPE,mountpoints",
            dev,
        ],
        capture_output=True,
        text=True,
    )
    print(ret)
    if ret and ret.returncode == 0 and "blockdevices" in ret.stdout:
        block_info = json.loads(ret.stdout)
        if "blockdevices" in block_info and block_info["blockdevices"]:
            block_info = block_info["blockdevices"][0]
            if "parttype" in block_info and block_info["parttype"]:
                dev["partname"] = translate_partition_type(dev["parttype"])
            if "children" in block_info and block_info["children"]:
                for child in block_info["children"]:
                    if "parttype" in child and child["parttype"]:
                        child["partname"] = translate_partition_type(child["parttype"])
            return block_info
    if not ret or not ret.stderr:
        print("Error: no return value from gathering block info")
    else:
        print("Error:", ret.stderr)
    return {}


if __name__ == "__main__":
    print(gather_block_info("/dev/sdc"))

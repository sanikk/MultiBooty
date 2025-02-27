import sys
import parted
import json

# TODO: Ok there is still some missing functionality but dog needs to get out. I'll finish this later.


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


def is_hybrid_iso(device_path):
    """
    Function that reads the first block from device
    and tries to determine if it's a hybrid ISO there.

    Returns True if there's a ISO 9660 sig there.
    """
    try:
        with open(device_path, "rb") as f:
            first_block = f.read(4096)
            if b"CD001" in first_block:  # ISO 9660 sig.
                return True
    except Exception as e:
        print(f"Error checking ISO signature: {e}")
    return False


def get_device_info(device_path):
    """
    Gather data with parted, using pyparted module.
    Requires (sudo) priviledges.

    Args
        device_path (str): path to the device, /dev/sdc

    Returns
        dict with the info
    """
    device = parted.getDevice(device_path)
    disk = parted.newDisk(device)

    info = {
        "device": device_path,
        "free_space": [(g.start, g.length) for g in disk.getFreeSpaceRegions()],
        "partitions": [
            {
                "number": p.number,
                "size": f"{p.getSize():.2f} MB",
                "start": p.geometry.start,
                "length": p.geometry.length,
                "type": translate_partition_type(p.type) if p.type else "Unknown",
            }
            for p in disk.partitions
        ],
        "hybrid_iso": is_hybrid_iso(device_path),
    }

    return info


if __name__ == "__main__":
    """
    Since this is run with sudo we just json dump this stuff.
    """
    devices = sys.argv[1:]
    device_infos = [get_device_info(dev) for dev in devices]
    print(json.dumps(device_infos, indent=4))

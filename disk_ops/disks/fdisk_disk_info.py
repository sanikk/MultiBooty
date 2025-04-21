from utils.runners import run_subprocess_with_sudo
import re


def parse_disk_info(disk_info: str) -> tuple:
    device_node = None
    sectors = None
    size = None
    fstype = None
    label = None
    sector_size = None
    for line in disk_info.split("\n"):
        if line.startswith("Disk model"):
            label = line.replace("Disk model: ", "").strip()
        elif line.startswith("Disk /") and line.endswith("sectors"):
            match = re.match(
                r"Disk (\S+): ([\d.]+\s+\w+), \d+ bytes, (\d+) sectors", line
            )
            if match:
                dev, size, sectors = match.groups()
                device_node = dev.strip()
                size = size.strip()
                sectors = int(sectors)
        elif line.startswith("Sector size"):
            match = re.search(r"(\d+)\s+bytes\s*/\s*(\d+)\s+bytes", line)
            if match:
                sector_size = int(match.group(2))
        elif line.startswith("Disklabel"):
            fstype = line.replace("Disklabel type: ", "")

    return (device_node, None, None, sectors, size, fstype, label, sector_size)


def parse_partition_info(partition_info: str) -> list[tuple | None]:
    if not partition_info:
        return []
    returnable = []
    for line in partition_info.split("\n"):
        if line.startswith("Device"):
            continue
        match = re.match(r"\s*(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(.+)", line)
        if match:
            device_node, start, end, sectors, size, fstype = match.groups()
            returnable.append((device_node, start, end, sectors, size, fstype))
    return returnable


def format_fdisk_output(output: str) -> tuple[tuple, list[tuple | None]] | None:
    try:
        disk_info, partition_info = output.split("\n\n")

        # partition_info = partition_info.split()
        parsed_disk_info = parse_disk_info(disk_info)
        parsed_partition_info = parse_partition_info(partition_info)
        return parsed_disk_info, parsed_partition_info
    except Exception as e:
        print(e)
        return None


def fdisk_read_info(device) -> tuple[tuple, list, list] | None:
    """
    Runner for the whole thing.
    Reads and parses fdisk -l output for the given device.

    Args
        device (str): the device to inspect

    Return
        tuple - ((disk), [partitions], [errors])
    """
    try:
        ret = run_subprocess_with_sudo("fdisk", ["-l", device])
        if ret and ret.returncode == 0:
            disk_info = format_fdisk_output(ret.stdout)
            if disk_info:
                return *disk_info, [
                    line.strip() for line in ret.stderr.split("\n") if line
                ]
    except Exception as e:
        print(e)
        return None

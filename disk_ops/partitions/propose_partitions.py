import parted
import sys
import json


def propose_partitions(dev: str, boot_size_mb: int) -> dict:
    """
    SUDO
    Partitions the dev with desired boot sector size.
    Does NOT commit changes to disk, just returns the values.

    Args
        dev (str): device to run on
        boot_size_mb (int): size of boot sector

    Returns
        dict with the partitioning info
    """
    device = parted.Device(dev)

    # Alignment with logical sectors
    alignment = device.optimumAlignment
    geom = parted.Geometry(device, start=0, length=device.length)
    test_sector = alignment.grainSize // 2 + 1
    aligned_up = alignment.alignUp(geom, test_sector)
    aligned_down = alignment.alignDown(geom, test_sector)

    logical_sector_size = device.sectorSize
    total_sectors = device.length
    disk_size_mb = device.getSize(unit="MB")

    boot_size_sectors = (boot_size_mb * 1024 * 1024) // logical_sector_size
    boot_start = aligned_up
    boot_end = alignment.alignDown(geom, boot_start + boot_size_sectors) - 1

    root_start = boot_end + 1
    root_end = (
        total_sectors
        if (total_sectors + 1) % alignment.grainSize == 0
        else alignment.alignDown(geom, total_sectors)
    )

    partition_info = {
        "device": dev,
        "sector_size": logical_sector_size,
        "total_sectors": total_sectors,
        "disk_size_mb": disk_size_mb,
        "alignment": {
            "minimum_grain_size": alignment.grainSize,
            f"align_up_test_{test_sector}": aligned_up,
            f"align_down_test_{test_sector}": aligned_down,
        },
        "partitions": [
            {
                "name": "EFI System Partition",
                "type": "fat32",
                "start": boot_start,
                "end": boot_end,
                "size_mb": (boot_end - boot_start)
                * logical_sector_size
                // (1024 * 1024),
            },
            {
                "name": "Root Partition",
                "type": "ext4",
                "start": root_start,
                "end": root_end,
                "size_mb": (root_end - root_start)
                * logical_sector_size
                / (1024 * 1024),
            },
        ],
    }
    return partition_info


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Invalid number of arguments: {len(sys.argv)} != 3", file=sys.stderr)
        sys.exit(1)

    partition_info = propose_partitions(sys.argv[1], int(sys.argv[2]))
    print(json.dumps(partition_info, indent=4))

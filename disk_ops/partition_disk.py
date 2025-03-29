import parted
import subprocess
import sys

from parted import geometry


def partition_disk(
    dev,
    boot_start,
    boot_end,
    root_start,
    root_end,
    # pttype="gpt", optimum=True
):
    # TODO: add possible error types to docstring here
    """
    SUDO
    Partitions the disk

    Args:
        dev (str): The device_node to partition ("/dev/sdX")
        boot_start (int): The start sector of boot partition
        boot_end (int): The end sector of boot partition
        root_start (int): The start sector of root partition
        root_end (int): The end sector of root partition
    Sketched args:
        pttype (str): The partition table type, "gpt" or "mbr"
        optimum (bool): Whether to use optimum values for sectors considering block size

    Returns:
        None: might throw an error
    """
    device = parted.Device(dev)
    disk = parted.freshDisk(device, "gpt")

    # geom = parted.Geometry(device, start=0, length=device.length)
    boot_geom = parted.Geometry(device, start=boot_start, end=boot_end)
    boot_partition = parted.Partition(
        disk,
        type=parted.PARTITION_NORMAL,
        fs=parted.FileSystem(type="fat32", geometry=boot_geom),
        geometry=boot_geom,
    )
    boot_partition.setFlag(parted.PARTITION_BOOT)
    boot_partition.setFlag(parted.PARTITION_ESP)
    # if optimum:
    # else:
    disk.addPartition(
        boot_partition, parted.Constraint(exactGeom=boot_partition.geometry)
    )
    root_geom = parted.Geometry(device, start=root_start, end=root_end)
    root_partition = parted.Partition(
        disk=disk,
        type=parted.PARTITION_NORMAL,
        fs=parted.FileSystem(type="ext4", geometry=root_geom),
        geometry=root_geom,
    )
    # if optimum:
    # else:
    disk.addPartition(
        root_partition, parted.Constraint(exactGeom=root_partition.geometry)
    )

    disk.commit()


if __name__ == "__main__":
    if len(sys.argv) not in [6, 7]:
        print("Invalid number of arguments: {len(sys.argv)}", file=sys.stderr)
        sys.exit(1)
    try:
        partition_disk(*[int(arg) if arg.isdigit() else arg for arg in sys.argv[1:]])
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(2)

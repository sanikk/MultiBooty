from pathlib import Path


def sysfs_exists():
    """
    Checks if the the sysfs system is found.

    Return
        bool - True if found
    """
    return Path("/sys/block").exists()


def collect_removable_devices() -> list[str]
    # [tuple[str, int, int, str]]:
    """
    Collects all devices with the removable flag that are connected.

    Return
        list - list of tuples with (device_node, number_of_sectors, sector_size)
    """
    return [dev.name for dev in Path("/sys/block").glob("sd*") if (dev / "removable").read_text().strip() == "1"]
    removables = [
        (
            dev.name,
            int(Path(dev / "size").read_text().strip()),
            int(Path(dev / "queue/hw_sector_size").read_text().strip()),
            f"{Path(dev / "device/vendor").read_text().strip()} {Path(dev / "device/model").read_text().strip()}",
        )
        for dev in Path("/sys/block").glob("sd*")
        if (dev / "removable").read_text().strip() == "1"
    ]
    return removables


def collect_partitions_for_device(dev: str) -> list:
    """
    Collects partitions for the given device.

    Return
        list - list of tuples (device_node, number_of_sectors, start_sector)
    """
    partitions = [
        (
            partition.name,
            int(Path(partition, "size").read_text().strip()),
            int(Path(partition, "start").read_text().strip()),
        )
        for partition in Path("/sys/block", dev).glob(f"{dev}*")
    ]
    return sorted(partitions)


def list_removable_devices() -> list:
    """
    Collects disks and partitions for the select_device UI component.

    Return
        list - list of tuples of tuples [(disk), (part1), (part2), ...]
    """
    devs = collect_removable_devices()
    partitions = [collect_partitions_for_device(dev[0]) for dev in devs]
    return [(dev, *partitions) for dev, partitions in zip(devs, partitions)]


if __name__ == "__main__":
    # devs = collect_removable_devices()
    # partitions = [collect_partitions_for_device(dev[0]) for dev in devs]
    # for dev, part in zip(devs, partitions):
    #     print(dev)
    #     for p in part:
    #         print(p)
    #     print("")
    # end_product = [(dev, *partitions) for dev, partitions in zip(devs, partitions)]
    # print(end_product)
    # for disk, *partitions in end_product:
    #     print(disk)
    #     for part in partitions:
    #         print(part)
    #     print("")
    lst = list_removable_devices()
    for disk, part1, part2, *rest in lst:
        print(disk)
        print(part1)
        print(part2)
        print(rest)

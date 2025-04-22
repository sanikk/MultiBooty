from pathlib import Path


def find_removable_devices() -> list[str | None]:
    # [tuple[str, int, int, str]]:
    """
    Collects all devices with the removable flag that are connected.

    Return
        list - list of tuples with (device_node, number_of_sectors, sector_size)
    """
    return [
        f"/dev/{dev.name}"
        for dev in Path("/sys/block").glob("sd*")
        if (dev / "removable").read_text().strip() == "1"
    ]

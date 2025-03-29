import fcntl, sys, struct, json


def get_usb_info(devices):
    """
    SUDO

    Gets sector size, number of sectors and size in bytes of given block devices

    Args:
        devices (list[str]): List of usb block devices

    Returns:
        dict[dict]: of block devices
        or
        dict: empty dict
    """
    device_infos = {}
    for device in devices:
        with open(device, "rb") as f:
            sector_size = struct.unpack("I", fcntl.ioctl(f, 0x1268, b"    "))[0]
            size_bytes = struct.unpack("Q", fcntl.ioctl(f, 0x80081272, b"        "))[0]
            num_sectors = size_bytes // sector_size
            device_infos[device] = {
                "sector_size": sector_size,
                "num_sectors": num_sectors,
                "size_bytes": size_bytes,
            }
    return device_infos


if __name__ == "__main__":
    if len(sys.argv) > 1:
        devices = sys.argv[1:]
        device_infos = get_usb_info(devices)
        if device_infos:
            print(json.dumps(device_infos, indent=4))
            sys.exit(0)
    sys.exit(1)

import fcntl, sys, struct, json


def get_usb_info(device):
    with open(device, "rb") as f:
        sector_size = struct.unpack("I", fcntl.ioctl(f, 0x1268, b"    "))[0]
        size_bytes = struct.unpack("Q", fcntl.ioctl(f, 0x80081272, b"        "))[0]
        num_sectors = size_bytes // sector_size
        return {
            "sector_size": sector_size,
            "num_sectors": num_sectors,
            "size_bytes": size_bytes,
        }


if __name__ == "__main__":
    devices = sys.argv[1:]
    device_infos = {dev: get_usb_info(dev) for dev in devices}
    print(json.dumps(device_infos, indent=4))

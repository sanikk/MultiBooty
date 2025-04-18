import pyudev


def get_all_block_devices() -> list[str]:
    """
    USERSPACE
    Get all connected USB block devices.

    Returns:
        Returns a list of /dev/sdX devices.

    Example:
        returns ["/dev/sdc"]
    """
    context = pyudev.Context()
    usb_devices = [
        device.device_node
        for device in context.list_devices(subsystem="block", DEVTYPE="disk")
        if device.device_node and device.get("ID_BUS") == "usb"
    ]
    return usb_devices


# monitor example. monitor for inserted devices.
# https://pyudev.readthedocs.io/en/latest/guide.html

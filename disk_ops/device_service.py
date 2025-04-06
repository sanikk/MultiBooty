from disk_ops.disks import block_devices
from disk_ops.disks.block_devices import get_all_block_devices
from disk_ops.disks.disk_runners import get_disk_info


class DeviceService:

    def __init__(self, device=None, number_of_sectors=None, sector_size=None):
        self._device = device
        self._number_of_sectors = number_of_sectors
        self._sector_size = sector_size

    def get_device(self):
        return self._device

    def get_number_of_sectors(self):
        return self._number_of_sectors

    def set_device(self, device, sector_size, number_of_sectors, size_in_bytes):
        self._device = device
        self._number_of_sectors = number_of_sectors
        self._sector_size = sector_size

    def list_devices(self):
        block_devices = get_all_block_devices()
        disk_info = get_disk_info(block_devices)
        return disk_info

import subprocess
from disk_ops.disks.block_devices import get_all_block_devices
from disk_ops.disks.disk_runners import get_disk_info, wait_device
from disk_ops.disks.gather_block_info import gather_block_info
from disk_ops.partitions.partition_runners import propose_partitions, make_partitions
from disk_ops.make_filesystems import (
    make_fat32_filesystem,
    make_ext4_filesystem,
)
import json


class DeviceService:

    def __init__(self, device=None, number_of_sectors=None, sector_size=None):
        self._device = device
        self._number_of_sectors = number_of_sectors
        self._sector_size = sector_size
        self._suggested_partititions = None
        self._boot_fs = "fat32"
        self._root_fs = "ext4"

    def get_device(self):
        return self._device

    def get_number_of_sectors(self):
        return self._number_of_sectors

    def set_device(self, device, sector_size, number_of_sectors, size_in_bytes):
        self._device = device
        self._number_of_sectors = number_of_sectors
        self._sector_size = sector_size

    def device_info(self):
        if not self._device:
            return "self._device not set?"
        disk_info = gather_block_info(self._device)
        return disk_info

    def list_devices(self):
        return get_disk_info(get_all_block_devices())

    def suggest_partitions(self, boot_size_mb):
        if not self._device:
            return
        partitions_info = propose_partitions(self._device, boot_size_mb)
        self._suggested_partititions = {
            "boot_start": partitions_info["partitions"][0]["start"],
            "boot_end": partitions_info["partitions"][0]["end"],
            "root_start": partitions_info["partitions"][1]["start"],
            "root_end": partitions_info["partitions"][1]["end"],
        }
        return partitions_info

    def make_partitions(self):
        if not self._device or not self._suggested_partititions:
            return
        make_partitions(self._device, **self._suggested_partititions)

    def make_boot_fs(self):
        """
        This needs udev to be populated with the new partitions. Or something like that.
        I use check before running this
        """
        make_fat32_filesystem(self._device, 1)

    def make_root_fs(self):
        make_ext4_filesystem(self._device, 2)

    def wait_for_partition(self, partition):
        wait_device(partition)

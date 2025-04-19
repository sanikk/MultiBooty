from disk_ops.disks.block_devices import get_all_block_devices
from disk_ops.disks.disk_runners import get_disk_info
from disk_ops.disks.gather_block_info import gather_block_info
from disk_ops.partitions.partition_runners import propose_partitions, make_partitions
from disk_ops.filesystem.filesystem_runners import (
    make_fat32_filesystem,
    make_ext4_filesystem,
    read_partition_uuid,
    make_root_folders,
)


class DeviceService:

    def __init__(self, device=None):
        self._device = device

        self._suggested_partititions = None
        self._boot_fs = "fat32"
        self._boot_uuid = None
        self._root_fs = "ext4"
        self._root_uuid = None

        self._mountpoint = None

    def get_device(self):
        return self._device

    def get_boot_uuid(self) -> str | None:
        if self._boot_uuid:
            return self._boot_uuid

    def get_root_uuid(self) -> str | None:
        if self._root_uuid:
            return self._root_uuid

    def set_device(
        self,
        device,
        *args,
    ):
        _ = args
        self._device = device

    def get_mountpoint(self) -> str | None:
        return self._mountpoint

    def set_mountpoint(self, mountpoint: str):
        self._mountpoint = mountpoint

    def device_info(self) -> dict[str, str]:
        if not self._device:
            return {"error": "self._device not set?"}
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
        make_fat32_filesystem(partition=f"{self._device}1")

    def make_root_fs(self):
        make_ext4_filesystem(f"{self._device}2")

    def read_boot_uuid(self) -> bool:
        if not self._device:
            return False
        ret = read_partition_uuid(f"{self._device}1")
        if ret:
            self._boot_uuid = ret
            return True
        return False

    def read_root_uuid(self) -> bool:
        if not self._device:
            return False

        ret = read_partition_uuid(f"{self._device}2")
        if ret:
            self._root_uuid = ret
            return True
        return False

    def make_roots_folders(self) -> bool:
        if not self._device or not self._mountpoint:
            print("args not set")
            return False
        return make_root_folders(
            partition=f"{self._device}2", mountpoint=self._mountpoint
        )

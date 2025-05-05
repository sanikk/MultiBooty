from disk_ops.disks.find_removable_devices import find_removable_devices

from disk_ops.disks.lsblk_tools import disk_info
from disk_ops.filesystem.filesystem_runners import (
    make_ext4_filesystem,
    make_ext2_filesystem,
    make_fat32_filesystem,
    make_fat16_filesystem,
)
from disk_ops.partitions.sgdisk_ops import (
    make_new_gpt,
    make_next_partition,
    make_hybrid_mbr,
    verify_gpt,
)


class DeviceService:

    _fat_fs_types = [
        ("fat32", make_fat32_filesystem),
        ("fat16", make_fat16_filesystem),
    ]

    _linux_fs_types = [
        ("ext4 no journal", make_ext4_filesystem),
        ("ext2", make_ext2_filesystem),
    ]

    def __init__(self, device: tuple | None = None):

        self._device = device
        self._all_devices = None
        self._device_info = None

        self._suggested_partititions = None

        self._boot_partition_size = 100
        self._boot_partition_fs = 0
        self._boot_partition_uuid = None

        self._package_partition = True
        self._package_partition_size = 2048
        self._package_partition_fs = 0
        self._package_partition_uuid = None

        self._root_fs = 0
        self._root_uuid = None

        self._hybrid_mbr = True

        self._mountpoint = "/mnt"

    def partition_disk(self):
        if not make_new_gpt(self._device):
            return False
        if not make_next_partition(self._device, size=self._boot_partition_size):
            return False
        if self._package_partition and not make_next_partition(
            self._device, size=self._package_partition_size
        ):
            return False

        if not make_next_partition(self._device):
            return False
        if self._hybrid_mbr and not make_hybrid_mbr(
            self._device, self._package_partition
        ):
            return False
        if not verify_gpt(device=self._device):
            return False
        return True

    # Device Functions

    def get_device(self):
        if self._device:
            return self._device
        return None

    def set_device(self, selection: int):
        if self._all_devices and 0 <= selection < len(self._all_devices):
            self._device_info = self._all_devices[selection]
            self._device = self._device_info[0][0]
            self._all_devices = None

    def get_device_info(self):
        return self._device_info

    def read_device_info(self) -> bool:
        if not self._device:
            return False
        ret = disk_info(self._device)
        if ret:
            self._device_info = ret
            return True
        return False

    def get_mountpoint(self) -> str | None:
        return self._mountpoint

    def set_mountpoint(self, mountpoint: str):
        self._mountpoint = mountpoint

    def list_devices(self):
        """
        Gets a list of tuples of all devices in system.
        Sets self._all_devices to the list.

        """
        devices = find_removable_devices()
        ret = [tuple(disk_info(device)) for device in devices if device]
        self._all_devices = ret
        return ret

    # Partition functions
    def get_boot_partition_size(self):
        return self._boot_partition_size

    def set_boot_partition_size(self, val: str):
        try:
            new_size = int(val)
            if 0 < new_size:
                self._boot_partition_size = new_size
                return True
        except ValueError:
            pass
        return False

    def get_root_fs(self) -> str:
        return self._linux_fs_types[self._root_fs][0]

    def get_linux_fs_types(self) -> list:
        return [a[0] for a in self._linux_fs_types]

    def set_root_fs(self, index: int):
        if 0 <= index < len(self._linux_fs_types):
            self._root_fs = index

    def get_boot_fs(self) -> str:
        return self._fat_fs_types[self._boot_partition_fs][0]

    def get_fat_fs_types(self) -> list:
        return [a[0] for a in self._fat_fs_types]

    def set_boot_fs(self, index: int):
        if 0 <= index < len(self._fat_fs_types):
            self._boot_fs = index

    def get_package_partition(self) -> bool:
        return self._package_partition

    def set_package_partition(self, val: bool):
        if val in (True, False):
            self._package_partition = val

    def get_package_partition_fs(self) -> str:
        return self._linux_fs_types[self._package_partition_fs][0]

    def set_package_partition_fs(self, index: int):
        if 0 <= index < len(self._linux_fs_types):
            self._package_partition_fs = index

    def get_package_partition_size(self):
        return self._package_partition_size

    def set_package_partition_size(self, size_str: str):
        try:
            size = int(size_str)
            if size > 0:
                self._package_partition_size = size
                return True
        except ValueError:
            pass
        return False

    def get_package_partition_info(self):
        if self._package_partition:
            return f"File system: {self._linux_fs_types[self._package_partition_fs][0]}, Size: {self._package_partition_size}"
        return f"{self._package_partition}"

    def get_hybrid_mbr(self):
        return self._hybrid_mbr

    def set_hybrid_mbr(self, val: bool):
        self._hybrid_mbr = val

    #     def device_info(self) -> None | tuple[tuple, list]:
    #         if not self._device:
    #             return None
    #         # disk_info = gather_block_info(self._device)
    #         disk_info = fdisk_read_info(self._device)
    #         return disk_info
    #     def get_boot_uuid(self) -> str | None:
    #         if self._boot_uuid:
    #             return self._boot_uuid
    #
    #     def get_root_uuid(self) -> str | None:
    #         if self._root_uuid:
    #             return self._root_uuid


#    def set_boot_fs(self, boot_fs: str):
#        self._boot_fs = boot_fs


#     def suggest_partitions(self, boot_size_mb):
#         if not self._device:
#             return
#         partitions_info = propose_partitions(self._device[0], boot_size_mb)
#         self._suggested_partititions = {
#             "boot_start": partitions_info["partitions"][0]["start"],
#             "boot_end": partitions_info["partitions"][0]["end"],
#             "root_start": partitions_info["partitions"][1]["start"],
#             "root_end": partitions_info["partitions"][1]["end"],
#         }
#         return partitions_info
#
#     def make_partitions(self):
#         if not self._device or not self._suggested_partititions:
#             return
#         make_partitions(self._device[0], **self._suggested_partititions)
#
#     def make_boot_fs(self):
#         """
#         This needs udev to be populated with the new partitions. Or something like that.
#         I use check before running this
#         """
#         make_fat32_filesystem(partition=f"{self._device}1")
#
#     def make_root_fs(self):
#         make_ext4_filesystem(f"{self._device}2")
#
#     def read_boot_uuid(self) -> bool:
#         if not self._device:
#             return False
#         ret = read_partition_uuid(f"{self._device}1")
#         if ret:
#             self._boot_uuid = ret
#             return True
#         return False
#
#     def read_root_uuid(self) -> bool:
#         if not self._device:
#             return False
#
#         ret = read_partition_uuid(f"{self._device}2")
#         if ret:
#             self._root_uuid = ret
#             return True
#         return False
#
#     def make_roots_folders(self) -> bool:
#         if not self._device or not self._mountpoint:
#             print("args not set")
#             return False
#         return make_root_folders(
#             partition=f"{self._device}2", mountpoint=self._mountpoint
#         )

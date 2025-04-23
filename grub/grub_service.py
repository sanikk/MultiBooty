from disk_ops.device_service import DeviceService
from grub.grub_runners import make_grub
from utils.read_file_from_mount import read_mounted_file


class GrubService:
    def __init__(self, device_service: DeviceService) -> None:
        self._device_service = device_service
        self._mountpoint = "/mnt"
        self._architecture = "amd64"
        self._boot_uuid = None
        self._root_uuid = None

    def set_mountpoint(self, value: str):
        self._mountpoint = value

    def set_architecture(self, value: str):
        self._architecture = value

    def install_grub(self):
        make_grub(
            partition=f"{self._device_service.get_device()}1",
            mountpoint=self._mountpoint,
            architecture=self._architecture,
        )

    def read_current_grub(self):
        ret = read_mounted_file(
            # read_file_from_mount(
            partition=f"{self._device_service.get_device()}1",
            mountpoint=self._mountpoint,
            path="boot/grub",
            filename="grub.cfg",
        )
        if not ret:
            return

        settings, entries = ret.split("\n\n\n")
        for entry in entries.split("\n\n"):
            print(entry)
            for line in entry.split("\n"):
                line = line.strip()
                if line.startswith("set mem"):
                    print(f"mem={line.split("=")[-1]}")
                if line.startswith("loopback"):
                    print(f"iso={line.split(" ")[-1].split("/")[-1]}")
                if line.startswith("linux"):
                    print(f"kernel_image={line.split(" ")[1].replace("(loop)", "")}")
                if line.startswith("initrd"):
                    print(f"initram_fs={line.split(" ")[1].replace("(loop)", "")}")
            print("###")

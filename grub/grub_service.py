from disk_ops import device_service
from disk_ops.device_service import DeviceService
from grub.grub_runners import make_grub


class GrubService:
    def __init__(self, device_service: DeviceService) -> None:
        self._device_service = device_service
        self._mountpoint = "/mnt"
        self._architecture = "amd64"
        pass

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

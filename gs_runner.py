from disk_ops.device_service import DeviceService
from grub.grub_service import GrubService

ds = DeviceService()
gs = GrubService(ds)
ds.set_device("/dev/sdc", 10, 10, 10)
ret = gs.read_current_grub()
# settings, entries = ret.split("\n\n\n")
# print(f"{settings=}")
# entries = entries.split("\n\n")
# print(f"{entries=}")

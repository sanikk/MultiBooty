from disk_ops.device_service import DeviceService


ds = DeviceService()
print(ds.list_devices())
print(ds.set_device(0))
print(ds.set_mountpoint("/mnt"))
# print(ds.make_roots_folders())
# print(f"{json.loads(ds.device_info().stdout)=}")
# print(f"{ds.suggest_partitions(100)=}")

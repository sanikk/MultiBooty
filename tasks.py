from invoke.tasks import task
from disk_ops.disk_info import get_disk_info
from disk_ops.block_devices import get_all_block_devices


@task
def start(_):
    print(get_disk_info(get_all_block_devices()))


@task
def gui(c):
    c.run("python3 start_gui.py")


@task
def blockdevices(_):
    print(get_all_block_devices())


@task
def diskinfo(_):
    print(get_disk_info(["/dev/sdc", "/dev/sdb"]))

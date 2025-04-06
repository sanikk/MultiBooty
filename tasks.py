from invoke.tasks import task
from disk_ops.disks.disk_runners import get_disk_info
from disk_ops.disks.block_devices import get_all_block_devices

from utils.runners import (
    run_python_subprocess_with_sudo,
)
from disk_ops.partitions.partition_runners import (
    propose_partitions,
    make_partitions,
)
from grub.grub_runners import make_grub
from utils.mounting import is_mounted, mounted


@task
def start(_):
    print(get_disk_info(get_all_block_devices()))


@task
def gui(c):
    c.run("python3 start_gui.py")


@task
def curses(c):
    c.run("python3 curses_ui.py", pty=True)


@task
def blockdevices(_):
    print(get_all_block_devices())


@task
def diskinfo(_):
    print(get_disk_info(["/dev/sdc", "/dev/sdb"]))


@task
def iso(c):
    c.run("python3 iso_tools/arch_iso.py", pty=True)


# 0         EFI System Partition               2048        208895      100.00      fat32          Y
# 1         Root Partition                     208896      30865408    14969.00    ext4
@task
def parttest(_):
    print(make_partitions("/dev/sdc", 2048, 208895, 208896, 30865408))


# @mounted
# def testfunc(partition, mountpoint):
#     print("hello")
#     input("halted..partition should be mounted now")
#


@task
def mounttest(_):
    print(run_python_subprocess_with_sudo("mnttest.py", [], ValueError, "blob"))


# def make_grub(partition: str, mountpoint: str, x64: bool = True):
@task
def grubtest(_):
    # print(make_grub(partition="/dev/sdc1", "/mnt", True))
    ret = make_grub(partition="/dev/sdc1", mountpoint="/mnt", x64=True)
    print(ret.stdout)
    print(ret.stderr)


@task
def ismountedtest(_):
    print(is_mounted("/mnt"))

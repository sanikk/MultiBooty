from invoke.tasks import task
from disk_ops import device_service
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
def dst(c):
    s = device_service.DeviceService()
    # print(s.list_devices())
    s.set_device("/dev/sdc", 10, 10, 10)
    print(s.device_info())
    # print(s.suggest_partitions(100))
    # print(s.device_info("/dev/sdc"))

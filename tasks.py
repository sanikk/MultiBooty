from invoke.tasks import task


@task
def start(_):
    # print(get_disk_info(get_all_block_devices()))
    pass


@task
def gui(c):
    c.run("python3 start_gui.py")


@task
def curses(c):
    c.run("python3 curses_ui.py", pty=True)


@task
def gst(c):
    c.run("python3 gs_runner.py")


@task
def dst(c):
    c.run("python3 test_ds.py")


@task
def fd(c):
    c.run("python3 fdisk_runner.py")

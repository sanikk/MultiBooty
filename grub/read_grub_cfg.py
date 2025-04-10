from utils.runners import run_python_subprocess_with_sudo


def read_grub_config(device):
    ret = run_python_subprocess_with_sudo("grub/grub_reader.py", [f"{device}1"])
    print(f"{ret=}")
    pass

from pathlib import Path
from utils.mounting import mounted


@mounted
def write_grub_cfg(partition, mountpoint, timeout, default, entries, path="boot/grub"):
    with open(Path(partition, path, "grub.cfg"), "w") as f:
        f.write(f"set timeout={timeout}\n")
        f.write(f"set default={default}\n\n")
        for entry in entries:
            for line in entry:
                f.write(f"{line}")

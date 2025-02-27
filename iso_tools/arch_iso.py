import pycdlib
from PySquashfsImage import SquashFsImage


def list_packages_from_arch_iso(iso_path):
    """
    Rips a list of packages from an Arch Linux installation ISO.

    Args:
        iso_path (str|Path): path to the ISO file.

    Returns:
        list of package names found on the ISO.
    """
    iso = pycdlib.pycdlib.PyCdlib()
    iso.open(iso_path)

    sfs_path = None
    for child in iso.list_children(iso_path="/ARCH/X86_64"):
        file_id = child.file_identifier().decode("utf-8")
        if file_id.startswith("AIROOTFS.SFS"):
            sfs_path = f"/ARCH/X86_64/{file_id}"
            break

    if not sfs_path:
        raise FileNotFoundError("AIROOTFS.SFS not found in the ISO.")

    sfs_data = bytearray()
    with iso.open_file_from_iso(iso_path=sfs_path) as f:
        sfs_data.extend(f.read())
    iso.close()
    with SquashFsImage.from_bytes(bytes(sfs_data)) as sfs_image:
        pacman_local_dir = sfs_image.select("/var/lib/pacman/local")
        if pacman_local_dir:
            return [entry.name for entry in pacman_local_dir.iterdir() if entry.is_dir]
    return None


if __name__ == "__main__":
    iso_path = "archlinux-2024.11.01-x86_64.iso"
    packages = list_packages_from_arch_iso(iso_path)
    print(packages)

import pycdlib
from pathlib import Path
import gzip


def list_packages_from_debian_iso(iso_path):
    iso_info = {"name": Path(iso_path).stem}
    (
        iso_info["distro"],
        iso_info["version"],
        iso_info["architecture"],
        iso_info["format"],
        iso_info["part"],
    ) = iso_info["name"].split("-")
    iso = pycdlib.PyCdlib()
    iso.open(iso_path)
    for dirname, dirlist, filelist in iso.walk(iso_path="/DISTS"):
        if filelist:
            for file in filelist:
                if file.startswith(("STABLE", "TESTING", "UNSTABLE")):
                    iso_info["release"] = dirlist[0]
                if file.startswith("PACKAGE"):
                    print(dirname, file)
                    packages_path = Path(dirname, file)
                    print(f"{packages_path=}")
                    with iso.open_file_from_iso(iso_path=packages_path.__str__()) as f:
                        with gzip.open(f, "rt", encoding="utf-8") as gf:
                            # iso_info[
                            package_data = gf.read()
                            # print(package_data[:100])
    #         print(item)

    #     for child in iso.list_children(iso_path="/DISTS"):
    #         if child.file_identifier() not in [b".", b".."] and child.is_dir():
    #             file_id = child.file_identifier().decode("utf-8")
    #             iso_info["release"] = file_id
    #     for child in iso.list_children(iso_path=f"/DISTS/{iso_info["release"]}"):
    #         if child.file_identifier() not in [b".", b".."] and child.is_dir():
    #             component = child.file_identifier().decode("utf-8")
    #             for gchild in iso.list_children(
    #                 iso_path=f"/DISTS/{iso_info["release"]}/{component}"
    #             ):
    #                 # /BINARY-{iso_info["architecture"].upper()}/"):
    #                 # if gchild.is_dir() and gchild.file_identifier() not in [b".", b".."]:
    #                 if gchild.file_identifier().startswith(b"BINARY"):
    #                     for ggc in iso.list_children(f"{gchild.iso_path()}"):
    #                         print(ggc)
    # with iso.open_file_from_iso(iso_path=f"{gchild.iso_path}/") as f:
    # dir = gchild.file_identifier().decode("utf-8")

    # print(gchild.file_identifier())

    iso.close()
    return iso_info


if __name__ == "__main__":
    print(list_packages_from_debian_iso("debian-12.8.0-i386-DVD-1.iso"))

import pycdlib
from pathlib import Path
import gzip
from email.parser import Parser


def parse_packages_file(packages_text):
    packages = packages_text.strip().split("\n\n")
    parsed_packages = {}
    for package in packages:
        msg = Parser().parsestr(package)
        parsed_packages[msg["Package"]] = {k: v for k, v in msg.items()}
    return parsed_packages


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
                            component = packages_path.parts[-3]
                            iso_info[component] = parse_packages_file(gf.read())  # type: ignore
    iso.close()
    return iso_info


if __name__ == "__main__":
    print(list_packages_from_debian_iso("debian-12.8.0-i386-DVD-1.iso"))

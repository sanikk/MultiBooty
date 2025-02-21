import subprocess
import json


def get_usb_info():
    result = subprocess.run(
        ["wmic", "diskdrive", "get", "BytesPerSector,Size", "/format:json"],
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    for drive in data["Value"]:
        sector_size = int(drive["BytesPerSector"])
        total_size = int(drive["Size"])
        num_sectors = total_size // sector_size
        return sector_size, num_sectors, total_size


if __name__ == "__main__":
    print(get_usb_info())

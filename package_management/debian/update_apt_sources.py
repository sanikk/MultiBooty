import urllib.request
from urllib.error import HTTPError


def download_with_progress(
    url, dest_path, progress_callback=None, stored_last_modified=None
):
    req = urllib.request.Request(url)
    if stored_last_modified:
        req.add_header("If-Modified-Since", stored_last_modified)
    try:
        with urllib.request.urlopen(req) as response:
            last_modified = response.headers.get("Last-Modified")
            print(f"{last_modified=}")
            total_size = int(response.headers.get("Content-Length", 0))
            bytes_downloaded = 0
            chunk_size = 8192

            with open(dest_path, "wb") as f:
                while chunk := response.read(chunk_size):
                    f.write(chunk)
                    bytes_downloaded += len(chunk)

                    if progress_callback:
                        progress_callback(bytes_downloaded, total_size)

    except HTTPError as e:
        if e.code == 304:
            print("No update needed")


def print_progress(downloaded, total):
    if total > 0:
        percent = (downloaded / total) * 100
        print(f"Downloaded: {downloaded}/{total} bytes ({percent:.2f}%)", end="\r")
        if percent == 100:
            print()


if __name__ == "__main__":
    download_with_progress(
        "http://deb.debian.org/debian/dists/bookworm/main/binary-amd64/Packages.gz",
        "Packages.gz",
        print_progress,
        # "Sat, 11 Jan 2025 09:46:33 GMT",
    )

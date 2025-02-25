# package_list_baseurl = "http://deb.debian.org/debian/dists/bookworm/main/binary-amd64/Packages.gz"
def get_debian_package_url(dist, architecture, component):
    return f"http://deb.debian.org/debian/dists/{dist}/{component}/binary-{architecture}/Packages.gz"


if __name__ == "__main__":
    print(get_debian_package_url("bookworm", "i386", "main"))

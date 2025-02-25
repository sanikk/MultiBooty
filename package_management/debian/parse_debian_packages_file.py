from email.parser import Parser


def parse_debian_packages_file(packages_text):
    packages = packages_text.strip().split("\n\n")
    parsed_packages = {}
    for package in packages:
        msg = Parser().parsestr(package)
        parsed_packages[msg["Package"]] = {k: v for k, v in msg.items()}
    return parsed_packages

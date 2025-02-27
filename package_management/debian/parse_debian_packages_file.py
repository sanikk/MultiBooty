from email.parser import Parser


def parse_debian_packages_file(packages_text):
    """
    Parses a debian-style Packages file.
    Uses email parser, since that's their structure.

    Args:
        packages_text (type): The insides of a Packages.gz file.

    Returns:
        parsed_packages: Description of the return value.

    """
    packages = packages_text.strip().split("\n\n")
    parsed_packages = {}
    for package in packages:
        msg = Parser().parsestr(package)
        parsed_packages[msg["Package"]] = {k: v for k, v in msg.items()}
    return parsed_packages

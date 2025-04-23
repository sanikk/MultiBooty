from pycdlib.pycdlib import PyCdlib


def rip_iso(iso_file):
    iso = PyCdlib()
    iso.open(iso_file)

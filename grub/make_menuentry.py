def make_menuentry(id: int, name: str, mem: int, iso_file: str):
    f"""
    /* id={id} */
    menuentry "{name}" {{
        insmod part_gpt
        insmod fat
        insmod ext2
        insmod loopback
        insmod linux
        set mem={mem}
        
        /* Mount ISO (assuming it's stored at /boot-isos/debian.iso on the ext partition) */
        loopback loop (hd1,2)/isos/{iso_file}
        linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=/isos/{iso_file}
        initrd (loop)/casper/initrd
    }}
    """

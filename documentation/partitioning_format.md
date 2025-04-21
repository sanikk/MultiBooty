## Partitioning format

Just sketching what I need to return from lsblk and

### show_partitions fields

- identifier (device node)
- name (label)
- fs/partition type
- start sector
- end sector
- size (bytes)

### lsblk
- NAME
- LABEL
- FSTYPE / PARTTYPE

### parted

#### Manual run
```bash
$ sudo parted /dev/sdc unit s print
Error: The backup GPT table is corrupt, but the primary appears OK, so that will be used.
OK/Cancel? ok                                                             
Model: JetFlash Transcend 16GB (scsi)
Disk /dev/sdc: 30867456s
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start    End        Size       File system  Name  Flags
 1      2048s    229375s    227328s    fat32              boot, esp
 2      229376s  30865408s  30636033s  ext2
```

#### machine-readable
```bash
$ sudo parted -m -s /dev/sdc unit s print
Error: The backup GPT table is corrupt, but the primary appears OK, so that will be used.
BYT;
/dev/sdc:30867456s:scsi:512:512:gpt:JetFlash Transcend 16GB:;
1:2048s:229375s:227328s:fat32::boot, esp;
2:229376s:30865408s:30636033s:ext2::;
```

### fdisk -l <dev>

```bash
$ sudo fdisk -l /dev/sdc
The backup GPT table is corrupt, but the primary appears OK, so that will be used.
Disk /dev/sdc: 14.72 GiB, 15804137472 bytes, 30867456 sectors
Disk model: Transcend 16GB  
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 1C35FA27-CFE5-4C0E-B718-952352DFB378

Device      Start      End  Sectors  Size Type
/dev/sdc1    2048   229375   227328  111M EFI System
/dev/sdc2  229376 30865408 30636033 14.6G Linux filesystem
```

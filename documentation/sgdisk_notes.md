## Sgdisk (and gdisk by extension)

### Making uefi that works on old non-uefi

```bash
sgdisk -t 3:ef02 /dev/sdb
sudo grub-install --boot-directory=/mnt/boot --force --target=i386-pc /dev/sdb   -v
```

### Make new partition

```bash
sgdisk --new:{part_num}:{start}:{end}
sgdisk -N:{part_num}:{start}:{end}
sgdisk --new:1:33:56654
```

```bash
sgdisk --largest-new={part_num}
sgdisk -N:{part_num}
```


### Leaving room for backup GPT table at end

Leave (at least) 33 sectors empty.


### Resizing partitions

0. unmount the partition

1. check the file system is clean

```bash
e2fsck -f /dev/sdXN
```
-f to force full check anyway

2. resize FS on the partition

```bash
resize2fs -M /dev/sdXN
resize2fs /dev/sdXN <size in blocks>
resize2fs /dev/sdb2 8196
```

3. resize the partition

```bash
sgdisk --resize=N:<size in sectors>
sgdisk --resize=2:121234
```

4. grow fs to partition size if it was smaller

```bash
resize2fs /dev/sdXN
resize2fs /dev/sdb2
```


### Alignment

```bash
sgdisk -D <dev>
```
prints the value used for alignment. Partitions should be multiples of this. Errors go to stderr and don't pollute stdout output.


### Validating it's all good

```bash
sgdisk -v <device>
```




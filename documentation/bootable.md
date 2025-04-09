# Bootable disk

## Parted and flags

### set flags

```bash
parted /dev/sdX set 1 esp on
parted /dev/sdX set 1 boot on
```

### check flags

```bash
parted /dev/sdX print
```

## EFI Bootloader Location

    Your grubx64.efi is in EFI/GRUB/, but some firmware expects it in EFI/BOOT/ as bootx64.efi.

    Try copying it:
```bash
cp EFI/GRUB/grubx64.efi EFI/BOOT/bootx64.efi
```
### Result
Ok now I can choose to uefi boot from the stick and it gets as far as grub console!
Previously I just ended back in bios.

"When you copied it to EFI/BOOT/bootx64.efi, your BIOS could find and boot it, as this is the default for removable media."


## Missing grub.cfg for EFI Mode

    Some setups expect grub.cfg in EFI/GRUB/. Try copying it there:

```bash
cp boot/grub/grub.cfg EFI/GRUB/
```

### Result
Ok this was in the wrong place to start with, as boot/grub.cfg.
Moved it to boot/grub/grub.cfg and now I can boot


## Check if the ESP (EFI System Partition) is correctly flagged

    Run lsblk -f and confirm the boot partition is labeled vfat with the esp flag.

    If missing, try setting it manually:

```bash
parted /dev/sdX set 1 esp on
```

### Result


## Secure Boot Disabled?

If Secure Boot is enabled, unsigned grubx64.efi may not run. Disable Secure Boot in firmware settings.

### Result


## Try Running grub-install Without --boot-directory

EFI GRUB doesn't use /boot/grub/, only EFI/GRUB/grubx64.efi. Try installing it like this:

```bash
grub-install --target=x86_64-efi --efi-directory=/mnt/boot --bootloader-id=GRUB
```

### Result


## Does the EFI Shell See GRUB?

    Boot into an EFI shell (if available in BIOS) and check if fs0:\EFI\GRUB\grubx64.efi exists.

    Manually boot it:

```EFI
fs0:\EFI\GRUB\grubx64.efi>
```

### Result



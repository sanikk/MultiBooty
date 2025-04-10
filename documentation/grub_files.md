# GRUB FILES

### EFI Bootloader

Using "--removable" option should make grub-install copy
EFI/GRUB/grubx64.efi to EFI/BOOT/bootx64.efi.

Instead of 
```bash
grub-install --target={target} --efi-directory={mountpoint} --bootloader-id=GRUB --boot-directory={mountpoint}/boot
```
Try running grub-install like this
```bash
grub-install --target=x86_64-efi --efi-directory=/mnt/boot --bootloader-id=GRUB
```
that is, without --boot-directory option.

Many firmware implementations expect a fallback as
/EFI/BOOT/bootx64.efi.

### grub.cfg

This file should be located at /boot/grub/grub.cfg

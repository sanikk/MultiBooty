## Multibooty
### Portable install media manager

Small app for making self-contained portable linux install media.

First goal is to let the user setup the media and boot into a linux installer. We boot straight into the ISO using loopbacks in grub. 

The second part is to have a package manager and local package repository for this.

### Usage case example:

You want to install Debian(s) somewhere with no/bad internet. You know you have to install 'Discord' there, which should be pretty up-to-date to function without
bypassing the version check. 

So before going to the place with no/bad internet you can slap an USB stick into your computer, put the latest Debian ISO there, use the package manager part to fetch all the packages needed to install the latest version of discord. This app should be able to figure out which packages need to be updated and load them on to the USB stick. 

When you are on location you can just connect the USB stick to a port, run the normal Debian installer and end up with a functioning system and functioning up-to-date discord.

## Instructions

Clone this repository. Use
```bash
poetry install
```
to install dependencies.

Use
```bash
poetry run invoke curses
```
to run the app with curses interface.

## Configuration:
### None of this has been implemented yet.
I don't want to parse HTML pages for lists of mirrors, because KISS.

So there are a few directories under the directory
package_lists
Just paste the host part of a mirror near you to

Debian
[List of mirrors](https://www.debian.org/mirror/list)
Where to paste: package_lists/debian/source.txt
Example: ftp.fi.debian.org

Arch
[List of mirrors](https://archlinux.org/mirrors/status/)
Where to paste: package_lists/arch/source.txt
Example: mirror.hosthink.net/archlinux

### TODO NOTICE

Ok using those mirror config files has NOT been implemented yet. For now you can just check out individual functions,
and edit the urls you want in by hand in the if __name__==... parts.
We'll get there when I have stuff tying these functions together, and paths from root are nicer to build.

Legalese:

## License

This project is licensed under the Apache License 2.0.

## Dependencies

This project uses PySide6 (Qt6), which is licensed under the LGPLv3. You can find the full text of the LGPLv3 license here.
Compliance

### To comply with the LGPLv3 when using PySide6, the following conditions apply:

    Dynamic Linking: This project dynamically links to PySide6 and does not bundle the Qt libraries statically. This ensures users can replace or modify the PySide6 library without restrictions.

    Modifications: If you modify PySide6 or use a modified version of the library, you must make the modified version available to your users as per the terms of the LGPLv3.

    License Acknowledgment: The LGPLv3 license text is included in this project, and by using this project, you agree to comply with the terms of that license.

### Additional Notes

    This project is open-source and non-commercial.
    If you distribute this project, you must also provide a copy of the Apache License 2.0 and the LGPLv3 license with it.
    You are free to contribute, fork, and modify the project, as long as you maintain the required attribution as per the Apache License 2.0 and comply with LGPLv3 terms.

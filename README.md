I'm trying to make this thing. We'll see how this goes.

## Configuration:
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

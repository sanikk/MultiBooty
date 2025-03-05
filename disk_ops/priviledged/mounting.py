from os import system


def mount_command(dev, mountpoint):
    system(f"mount {dev} {mountpoint}")


def unmount_command(dev):
    system(f"unmount {dev}")


def mounted(dev):
    def decorator(func):
        def wrapper(*args, **kwargs):
            mount_command(dev, "/mnt")
            try:
                return func(dev, *args, **kwargs)  # Inject dev into the function
            finally:
                unmount_command(dev)

        return wrapper

    return decorator

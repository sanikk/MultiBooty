import os, time


def wait_for_device(path: str, timeout=10):
    for _ in range(int(timeout * 10)):
        if os.path.exists(path):
            try:
                with open(path, "rb"):
                    return True  # Successfully opened
            except OSError:
                pass  # Exists but not ready yet
        time.sleep(0.1)

    raise RuntimeError(f"Timeout waiting for device {path} to appear.")

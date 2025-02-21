import sys
from PySide6.QtWidgets import QApplication, QWidget

from gui.gui import GUI

# from device_service.device_service import DeviceService


def main():
    app = QApplication([])
    #     device_service = DeviceService()
    ui = GUI()
    ui.setWindowTitle("MultiBoot USB")
    ui.show()
    return sys.exit(app.exec())


if __name__ == "__main__":
    main()

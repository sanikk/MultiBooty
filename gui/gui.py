from gui.device_tab import DeviceTab
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget


class GUI(QWidget):
    def __init__(
        self,
        # , device_service
    ):
        super().__init__()
        layout = QVBoxLayout()
        self.tab_window = TabWindow()
        layout.addWidget(self.tab_window)
        self.setLayout(layout)


class TabWindow(QTabWidget):

    # TODO: make resizable like this
    # https://doc.qt.io/qt-6/qsizegrip.html
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        device_tab = DeviceTab()
        self.addTab(device_tab, "device tab")

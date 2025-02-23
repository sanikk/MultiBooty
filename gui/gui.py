from gui.device_tab import DeviceTab
from gui.iso_tab import IsoTab
from gui.local_package_tab import LocalPackageTab
from gui.remote_package_tab import RemotePackageTab
from gui.settings_tab import SettingsTab

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
        iso_tab = IsoTab()
        self.addTab(iso_tab, "iso tab")
        remote_package_tab = RemotePackageTab()
        self.addTab(remote_package_tab, "remote package tab")
        local_package_tab = LocalPackageTab()
        self.addTab(local_package_tab, "local package tab")
        settings_tab = SettingsTab()
        self.addTab(settings_tab, "settings tab")

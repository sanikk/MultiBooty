from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QTableWidget

from gui.common import get_table


class DeviceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QVBoxLayout()
        title_label = QLabel("Select a device from the list")
        layout.addWidget(title_label)
        self.table = get_table(self, ["device_node", "size", "sectors", "sector_size"])
        layout.addWidget(self.table)
        self.setLayout(layout)

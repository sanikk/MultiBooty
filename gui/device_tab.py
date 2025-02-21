from PySide6.QtWidgets import QVBoxLayout, QWidget, QTableWidget


class DeviceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QVBoxLayout()
        self.table = self.get_device_table()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def get_device_table(self):
        table = QTableWidget()
        table.setRowCount(10)
        table_labels = ("device_node", "size", "sectors", "sector_size")
        table.setColumnCount(len(table_labels))
        table.setHorizontalHeaderLabels(table_labels)
        return table

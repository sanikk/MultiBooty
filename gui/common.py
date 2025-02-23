from PySide6.QtWidgets import QTableWidget


def get_table(parent, labels: list[str]):
    table = QTableWidget(parent=parent)
    table.setRowCount(10)
    table.setColumnCount(len(labels))
    table.setHorizontalHeaderLabels(labels)
    return table

from PySide6.QtWidgets import QComboBox, QVBoxLayout, QWidget


class RemotePackageTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QVBoxLayout()
        self.distro_selector = QComboBox()
        layout.addWidget(self.distro_selector)
        self.version_selector = QComboBox()
        layout.addWidget(self.version_selector)
        self.setLayout(layout)
        pass

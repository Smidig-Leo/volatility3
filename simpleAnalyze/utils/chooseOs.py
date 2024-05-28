from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox
from PyQt5.QtCore import pyqtSignal

class ChooseOs(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent

        self.layout = QVBoxLayout()

        self.os_dropdown = QComboBox()
        self.os_dropdown.addItem("Windows")
        self.os_dropdown.addItem("Linux")
        self.os_dropdown.addItem("Mac")
        self.layout.addWidget(self.os_dropdown)
        self.setLayout(self.layout)


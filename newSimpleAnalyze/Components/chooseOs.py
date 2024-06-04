from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QWidget, QPushButton, \
    QHBoxLayout
from PyQt5.uic import  loadUi
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os


class ChooseOs(QMainWindow):
    os_changed = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('screens/ui/Os.ui', self)
        # self.parent_widget = parent
        #
        # self.layout = QVBoxLayout()
        #
        # self.windows_radio = QRadioButton('Windows')
        # self.linux_radio = QRadioButton('Linux')
        # self.mac_radio = QRadioButton('Mac')
        #
        # self.windows_radio.clicked.connect(lambda: self.on_os_changed("windows"))
        # self.linux_radio.clicked.connect(lambda: self.on_os_changed("linux"))
        # self.mac_radio.clicked.connect(lambda: self.on_os_changed("mac"))
        #
        # self.layout.addWidget(self.windows_radio)
        # self.layout.addWidget(self.linux_radio)
        # self.layout.addWidget(self.mac_radio)
        #
        # self.setLayout(self.layout)
        #
        # self.windows_radio.setChecked(True)

    def on_os_changed(self, text):
        print("Selected OS:", text)
        self.os_changed.emit(text)





from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QWidget, QPushButton, \
    QHBoxLayout
from PyQt5.uic import  loadUi
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os


class ChooseOs(QMainWindow):
    os_changed = pyqtSignal(str)

    def __init__(self, session_manager):
        super().__init__()
        loadUi('screens/ui/Os.ui', self)

        self.session_manager = session_manager

        if self.session_manager.get_os() == "":
            self.session_manager.set_os("windows")


        self.on_os_changed(self.session_manager.get_os())

        if self.session_manager.get_os() == "windows":
            self.radioButtonWindows.setChecked(True)
        elif self.session_manager.get_os() == "linux":
            self.radioButtonLinux.setChecked(True)
        elif self.session_manager.get_os() == "mac":
            self.radioButtonMac.setChecked(True)

        self.radioButtonWindows.clicked.connect(lambda: self.on_os_changed("windows"))
        self.radioButtonMac.clicked.connect(lambda: self.on_os_changed("mac"))
        self.radioButtonLinux.clicked.connect(lambda: self.on_os_changed("linux"))

    def on_os_changed(self, text):
        print("Selected OS:", text)
        self.session_manager.set_os(text)
        self.os_changed.emit(text)








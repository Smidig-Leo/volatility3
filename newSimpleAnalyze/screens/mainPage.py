from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.uic import  loadUi
from newSimpleAnalyze.Components.chooseOs import ChooseOs

class MainPage(QWidget):
    analyzedButtonClicked = pyqtSignal()
    def __init__(self, file_uploader, os):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.os = os
        self.file_uploader = file_uploader

        self.file_uploader.analyzedButtonClicked.connect(self.on_analyze_button_clicked)

        self.layout.addWidget(self.os)
        self.layout.addWidget(self.file_uploader)

    def on_analyze_button_clicked(self):
        self.analyzedButtonClicked.emit()





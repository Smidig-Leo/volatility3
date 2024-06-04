from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget
from PyQt5.uic import  loadUi
from newSimpleAnalyze.Components.fileUploader import FileUploader
from newSimpleAnalyze.Components.chooseOs import ChooseOs

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.os = ChooseOs()
        self.file_uploader = FileUploader()


        self.layout.addWidget(self.os)
        self.layout.addWidget(self.file_uploader)




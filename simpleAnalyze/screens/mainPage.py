from PyQt5.QtWidgets import QWidget, QVBoxLayout
from simpleAnalyze.utils.fileUploader import FileUploader

class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.file_uploader = FileUploader(parent)
        layout.addWidget(self.file_uploader)

        self.setLayout(layout)

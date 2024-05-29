from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSignal
from simpleAnalyze.utils.fileUploader import FileUploader
from simpleAnalyze.utils.chooseOs import ChooseOs

class MainPage(QWidget):
    file_path_set = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.file_uploader = FileUploader(parent)
        self.file_uploader.file_path_updated.connect(self.update_file_path)
        self.chooseOs = ChooseOs(parent)
        layout.addWidget(self.file_uploader)
        layout.addWidget(self.chooseOs)

        self.setLayout(layout)

    def update_file_path(self, file_path):
        self.file_path = file_path
        self.file_path_set.emit(file_path)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump")
        if file_path:
            self.update_file_path(file_path)

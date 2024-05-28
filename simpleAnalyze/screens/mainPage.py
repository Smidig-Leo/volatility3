from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal
from simpleAnalyze.utils.fileUploader import FileUploader

class MainPage(QWidget):
    file_path_set = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.file_uploader = FileUploader(parent)
        layout.addWidget(self.file_uploader)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"Selected file: {self.file_path}")
            self.file_path_set.emit(file_path)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os

class FileUploader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent

        self.layout = QVBoxLayout()


        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


        self.drop_area = QWidget()
        self.drop_area_layout = QVBoxLayout()
        self.drop_area.setLayout(self.drop_area_layout)
        self.drop_area.setFixedSize(300, 300)
        self.drop_area.setStyleSheet("""
            QWidget {
                background-color: black;
                border-radius: 15px;
                border: none;
            }
        """)

        self.drop_label = QLabel("Drag & Drop to upload file")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
            }
        """)

        self.or_label = QLabel("OR")
        self.or_label.setAlignment(Qt.AlignCenter)
        self.or_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                margin-top: 10px;
                margin-bottom: 10px;
            }
        """)

        self.select_button = QPushButton("Browse File")
        self.select_button.clicked.connect(self.select_file)
        self.select_button.setFixedSize(150, 40)
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: orange;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff9933;
            }
        """)

        self.drop_area_layout.addWidget(self.drop_label, alignment=Qt.AlignCenter)
        self.drop_area_layout.addWidget(self.or_label, alignment=Qt.AlignCenter)
        self.drop_area_layout.addWidget(self.select_button, alignment=Qt.AlignCenter)


        self.files_layout = QVBoxLayout()
        self.drop_area_layout.addLayout(self.files_layout)

        self.layout.addWidget(self.drop_area, alignment=Qt.AlignCenter)


        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setAcceptDrops(True)
        self.setLayout(self.layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            file_path = urls[0].toLocalFile()
            self.update_file_path(file_path)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump")
        if file_path:
            self.update_file_path(file_path)

    def update_file_path(self, file_path):
        self.file_path = file_path
        file_name = os.path.basename(file_path)
        self.add_file_label(file_name)
        if self.parent_widget and hasattr(self.parent_widget, 'plugin_screen'):
            self.parent_widget.plugin_screen.file_path = self.file_path
            self.parent_widget.plugin_screen.file_label.setText(f"Selected file: {file_name}")

    def add_file_label(self, file_name):
        file_label = QLabel(file_name)
        file_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                padding: 1px;
                border-radius: 5px;
                margin-top: 5px;
            }
        """)
        self.files_layout.addWidget(file_label)
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QWidget, QPushButton, \
    QHBoxLayout, QFrame
from PyQt5.uic import  loadUi
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os

from simpleAnalyze.utils.uploadConfirmation import is_valid_memory_dump, is_file_exists


# from simpleAnalyze.utils.uploadConfirmation import is_valid_memory_dump, is_file_exists


class FileUploader(QMainWindow):
    file_path_updated = pyqtSignal(list)
    analyzedButtonClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        loadUi('screens/ui/FileUploader.ui', self)

        # available buttons:
        # self.selectButton
        # self.fileName
        # self.deleteBtn
        # self.analyzeButton
        # self.fileUploaded

        self.file_paths = []
        self.file_uploaded_label = None
        self.file_widgets = {}

        self.dropArea.setAcceptDrops(True)

        self.selectButton.clicked.connect(self.select_file)

        self.dropArea.dragEnterEvent = self.dragEnterEvent
        self.dropArea.dropEvent = self.dropEvent

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            file_path = urls[0].toLocalFile()
            if is_valid_memory_dump(file_path) and is_file_exists(file_path):
                self.add_file_path(file_path)
            else:
                QMessageBox.critical(self, "Error",
                                     "The file you selected is not a valid memory dump! Please select a valid file.\n(Supported file extensions: .vmem)")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump")
        if file_path:
            if is_valid_memory_dump(file_path) and is_file_exists(file_path):
                self.add_file_path(file_path)
            else:
                QMessageBox.critical(self, "Error",
                                     "The file you selected is not a valid memory dump! Please select a valid file.\n(Supported file extensions: .vmem)")

    def add_file_path(self, file_path):
        if file_path not in self.file_paths:
            self.file_paths.append(file_path)
            self.add_file_label(file_path)
            self.file_path_updated.emit(self.file_paths.copy())
            self.show_popup(os.path.basename(file_path))
        else:
            print(f"File path {file_path} already exists in the list")

    def add_file_label(self, file_path):
        file_name = os.path.basename(file_path)
        print(f"Adding file label for: {file_name}")

        parentFrame = QFrame()

        frame1 = QFrame()
        frame2 = QFrame()

        label = QLabel(file_name)
        button = QPushButton("X")

        button.setStyleSheet("""
            QPushButton {
                border-radius:2px;
                background-color:red;
                max-width:20px;
                height:20px;
            }
        """)

        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()

        layout1.addWidget(label)
        layout2.addWidget(button)

        frame1.setLayout(layout1)
        frame2.setLayout(layout2)

        layout1.setAlignment(Qt.AlignRight)

        parentLayout = QHBoxLayout()
        parentLayout.addWidget(frame1)
        parentLayout.addWidget(frame2)

        parentFrame.setLayout(parentLayout)


        self.fileUploaderFrame.layout().addWidget(parentFrame)


    def show_popup(self, file_name):

        file_label = QLabel(file_name)
        file_label.setAlignment(Qt.AlignCenter)
        file_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
            }
        """)
        self.uploadedFiles.layout().addWidget(file_label)

        self.analyzeButton.setText("Analyze My Data")
        self.analyzeButton.setStyleSheet("""
            QPushButton {
                background-color:#F27821;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff9933;
            }
        """)

        self.analyzeButton.clicked.connect(self.emit_analyzeButtonClicked)


    def delete_file(self, file_path):
        print(f"Deleting file: {file_path}")
        if file_path in self.file_paths:
            self.file_paths.remove(file_path)
            print(f"Removed file path: {file_path}")
            if file_path in self.file_widgets:
                file_layout = self.file_widgets.pop(file_path)
                while file_layout.count():
                    item = file_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()

            if self.file_uploaded_label and self.file_uploaded_label.text().startswith(os.path.basename(file_path)):
                self.file_uploaded_label.clear()
                for i in reversed(range(self.layout.count())):
                    widget = self.layout.itemAt(i).widget()
                    if widget is not None and widget.objectName() == "popup_widget":
                        self.layout.removeWidget(widget)
                        widget.deleteLater()

            self.file_path_updated.emit(self.file_paths.copy())
            if self.parent_widget and hasattr(self.parent_widget, 'plugin_screen'):
                self.parent_widget.plugin_screen.clear_file_path()
            if self.parent_widget:
                self.parent_widget.session_manager.set_file_uploaded(self.file_paths)

    def emit_analyzeButtonClicked(self):
        self.analyzedButtonClicked.emit()

    def get_file_paths(self):
        return self.file_paths

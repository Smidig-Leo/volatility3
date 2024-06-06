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

        button.clicked.connect(lambda: self.delete_file(file_path))

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

        if len(self.file_paths) == 1:
            analyze_button = QPushButton("Analyze My Data")
            analyze_button.setStyleSheet("""
                QPushButton {
                    background-color:#F27821;
                    color: white;
                    font-size: 16px;
                    border: none;
                    border-radius: 5px;
                    width: 200px;
                    height: 24px;
                }
                QPushButton:hover {
                    background-color: #ff9933;
                }
            """)

            self.analyzeButtonFrame.layout().addWidget(analyze_button)

            analyze_button.clicked.connect(self.emit_analyzeButtonClicked)

    def delete_file(self, file_path):
        if file_path in self.file_paths:
            self.file_paths.remove(file_path)
            if not self.file_paths:  # If file_paths list is empty
                self.delete_analyze_button()

        for i in range(self.fileUploaderFrame.layout().count()):
            parentFrame = self.fileUploaderFrame.layout().itemAt(i).widget()
            if parentFrame:
                innerLayout = parentFrame.layout()
                if innerLayout:
                    innerFrameLabel = innerLayout.itemAt(0).widget()  # Access the inner frame
                    innerFrameButton = innerLayout.itemAt(1).widget()
                    if innerFrameLabel and innerFrameButton:
                        file_name_label = innerFrameLabel.layout().itemAt(0).widget()  # Access the label inside the inner frame
                        delete_button = innerFrameButton.layout().itemAt(0).widget()  # Access the delete button
                        if file_name_label and file_name_label.text() == os.path.basename(file_path):
                            delete_button.clicked.disconnect()  # Disconnect button signal
                            parentFrame.deleteLater()  # Delete the entire frame
                            # Remove label from the uploadedFiles layout
                            for j in range(self.uploadedFiles.layout().count()):
                                label = self.uploadedFiles.layout().itemAt(j).widget()
                                if label and label.text() == os.path.basename(file_path):
                                    label.deleteLater()
                                    break
                            break

        self.file_path_updated.emit(self.file_paths.copy())

    def delete_analyze_button(self):
        analyze_button = self.analyzeButtonFrame.layout().itemAt(0).widget()
        if analyze_button:
            analyze_button.deleteLater()

    def emit_analyzeButtonClicked(self):
        self.analyzedButtonClicked.emit()

    def get_file_paths(self):
        return self.file_paths

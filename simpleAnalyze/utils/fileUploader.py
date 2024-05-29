from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSpacerItem, QSizePolicy, \
    QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os
from simpleAnalyze.utils.uploadConfirmation import is_valid_memory_dump, is_file_exists

class FileUploader(QWidget):
    file_path_updated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.file_path = None

        self.file_uploaded_label = None
        self.layout = QVBoxLayout()

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.drop_area = QWidget(self)
        self.drop_area.setAcceptDrops(True)
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

        self.setLayout(self.layout)

        self.drop_area.dragEnterEvent = self.dragEnterEvent
        self.drop_area.dropEvent = self.dropEvent

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            file_path = urls[0].toLocalFile()
            if is_valid_memory_dump(file_path) and is_file_exists(file_path):
                self.update_file_path(file_path)
            else:
                QMessageBox.critical(self, "Error",
                                     "The file you selected is not a valid memory dump! Please select a valid file.\n(Supported file extensions: .vmem)")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump")
        if file_path:
            if is_valid_memory_dump(file_path) and is_file_exists(file_path):
                self.update_file_path(file_path)
            else:
                QMessageBox.critical(self, "Error",
                                     "The file you selected is not a valid memory dump! Please select a valid file.\n(Supported file extensions: .vmem)")

    def update_file_path(self, file_path):
        self.file_path = file_path
        file_name = os.path.basename(file_path)
        self.add_file_label(file_name)
        self.show_popup(file_name)
        if self.parent_widget and hasattr(self.parent_widget, 'plugin_screen'):
            self.parent_widget.plugin_screen.file_path = self.file_path
            self.parent_widget.plugin_screen.file_label.setText(f"Selected file: {file_name}")
            # Call SessionManager to store the uploaded file path
            if self.parent_widget:
                self.parent_widget.session_manager.set_file_uploaded(file_path)
        self.file_path_updated.emit(file_path)

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

    def add_file_label(self, file_name):
        file_layout = QHBoxLayout()

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

        delete_button = QPushButton("X")
        delete_button.clicked.connect(lambda _, name=file_name: self.delete_file(name))
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 12px;
                padding: 3px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)

        file_layout.addWidget(file_label)
        file_layout.addWidget(delete_button)
        self.files_layout.addLayout(file_layout)

    def show_popup(self, file_name):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None and widget.objectName() == "popup_widget":
                self.layout.removeWidget(widget)
                widget.deleteLater()

        popup_widget = QWidget()
        popup_widget.setObjectName("popup_widget")
        popup_layout = QVBoxLayout()
        popup_widget.setLayout(popup_layout)

        popup_widget.setStyleSheet("""
            QWidget#popup_widget {
                background-color: #343534;
                padding: 20px;
            }
        """)

        self.file_uploaded_label = QLabel(f"{file_name} \n uploaded")  # Store the reference
        self.file_uploaded_label.setAlignment(Qt.AlignCenter)
        self.file_uploaded_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
            }
        """)

        analyze_button = QPushButton("Analyze My Data")
        analyze_button.setFixedSize(150, 40)
        analyze_button.setStyleSheet("""
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
        analyze_button.clicked.connect(self.go_to_analyze_screen)

        popup_layout.addWidget(self.file_uploaded_label)  # Use the reference
        popup_layout.addWidget(analyze_button, alignment=Qt.AlignCenter)

        self.layout.addWidget(popup_widget, alignment=Qt.AlignCenter)

    def delete_file(self, file_name):
        for i in reversed(range(self.files_layout.count())):
            layout_item = self.files_layout.itemAt(i)
            if layout_item is not None:
                layout = layout_item.layout()
                if layout is not None:
                    label_item = layout.itemAt(0)
                    if label_item is not None:
                        label_widget = label_item.widget()
                        if label_widget is not None and label_widget.text() == file_name:
                            widget_to_remove = self.files_layout.itemAt(i).layout()
                            if widget_to_remove is not None:
                                for j in reversed(range(widget_to_remove.count())):
                                    file_widget = widget_to_remove.itemAt(j).widget()
                                    if file_widget is not None:
                                        file_widget.deleteLater()
                                widget_to_remove.deleteLater()

        if self.file_uploaded_label and self.file_uploaded_label.text().startswith(file_name):
            self.file_uploaded_label.clear()

        if self.file_path == file_name:
            self.file_path = None
            self.file_path_updated.emit("")
    def go_to_analyze_screen(self):
        if self.parent_widget:
            self.parent_widget.show_analyzed_data_screen()

    def get_file_path(self):
        return self.file_path

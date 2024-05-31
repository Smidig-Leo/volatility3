import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QCheckBox
from PyQt5.QtCore import pyqtSignal, Qt
from simpleAnalyze.utils.fileUploader import FileUploader


class SelectDump(QWidget):
    file_selected = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.file_paths = []
        layout = QVBoxLayout()
        self.file_uploader = FileUploader()
        self.file_uploader.file_path_updated.connect(self.update_file_paths)
        self.file_label = QLabel("DUMPS")
        layout.addWidget(self.file_label)
        self.dump_list = QListWidget()
        layout.addWidget(self.dump_list)
        self.setLayout(layout)
        self.apply_styles()
        self.populate_dump_list()

    def update_file_paths(self, file_paths):
        self.file_paths = file_paths
        self.populate_dump_list()
        print("Received file paths:", file_paths)

    def apply_styles(self):
        self.file_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 18px;
                padding: 10px;
            }
        """)
        self.dump_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                padding: 5px;
            }
            QListWidget::item {
                color: black;
                padding: 10px;
                border-bottom: 1px solid #ccc;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)

    def populate_dump_list(self):
        self.dump_list.clear()
        for file_path in self.file_paths:
            display_text = os.path.basename(file_path)
            self.add_list_item(display_text, file_path)

    def add_list_item(self, display_text, file_path):
        item = QListWidgetItem()
        widget = QWidget()
        layout = QVBoxLayout()
        checkbox = QCheckBox()
        checkbox.stateChanged.connect(lambda state: self.on_checkbox_state_changed(state, file_path))
        layout.addWidget(checkbox)
        layout.addWidget(QLabel(display_text))
        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        item.setData(Qt.UserRole, file_path)
        self.dump_list.addItem(item)
        self.dump_list.setItemWidget(item, widget)
        print(f"Added item: {display_text} with file path: {file_path}")

    def on_checkbox_state_changed(self, state, file_path):
        if state == Qt.Checked:
            self.file_selected.emit([file_path])

    def get_selected_files(self):
        selected_files = []
        for index in range(self.dump_list.count()):
            item = self.dump_list.item(index)
            widget = self.dump_list.itemWidget(item)
            checkbox = widget.findChild(QCheckBox)
            if checkbox.isChecked():
                file_path = item.data(Qt.UserRole)
                selected_files.append(file_path)
        return selected_files



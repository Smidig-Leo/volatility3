import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QCheckBox, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt


class SelectDump(QWidget):
    file_selected = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.file_paths = []
        layout = QVBoxLayout()
        self.file_label = QLabel("DUMPS")
        layout.addWidget(self.file_label)
        self.dump_list = QListWidget()
        layout.addWidget(self.dump_list)
        self.setLayout(layout)
        self.apply_styles()

    def update_file_paths(self, list_of_files):
        self.file_paths = list_of_files
        self.populate_dump_list()
        print("Received file paths:", list_of_files)

    def apply_styles(self):
        self.file_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                padding: 0px;
                border-bottom: 1px solid #F27821;
            }
        """)
        self.dump_list.setStyleSheet("""
            QListWidget {
                border-radius: 5px;
                background-color: #343534;
                color: white;
                border: none;
                padding: 0px;
            }
            QListWidget::item {
                color: white;
                height: 25px;
                padding: 0px;
                border: none;
                background-color: #343534;
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
        layout = QHBoxLayout()
        checkbox = QCheckBox()
        checkbox.stateChanged.connect(lambda state, fp=file_path: self.on_checkbox_state_changed(state, fp))

        label = QLabel(display_text)
        label.setStyleSheet("color: white;")
        checkbox.setStyleSheet("""
                        QCheckBox::indicator {
                            width: 10px;
                            height: 10px;
                            border-radius: 3px;
                        }
                        QCheckBox::indicator:unchecked {
                            background-color: white;
                            border: 1px solid #ccc;
                        }
                        QCheckBox::indicator:checked {
                            background-color: #F27821;
                            border: 1px solid #F27821;
                        }
                    """)
        layout.addWidget(checkbox)
        layout.addWidget(label)
        layout.addStretch()
        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        item.setData(Qt.UserRole, file_path)
        self.dump_list.addItem(item)
        self.dump_list.setItemWidget(item, widget)
        print(f"Added item: {display_text} with file path: {file_path}")

    def on_checkbox_state_changed(self, state, file_path):
        selected_files = self.get_selected_files()
        self.file_selected.emit(selected_files)

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

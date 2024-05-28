from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.file_label = QLabel("No memory dump selected")
        layout.addWidget(self.file_label)

        self.select_button = QPushButton("Select Memory Dump")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"Selected file: {self.file_path}")
            self.parent().plugin_screen.file_path = self.file_path
            self.parent().plugin_screen.file_label.setText(f"Selected file: {self.file_path}")

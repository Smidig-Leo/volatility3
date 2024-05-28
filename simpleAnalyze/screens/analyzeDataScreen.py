from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class AnalyzeDataScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.output_text = QTextEdit()
        layout.addWidget(self.output_text)

        self.setLayout(layout)
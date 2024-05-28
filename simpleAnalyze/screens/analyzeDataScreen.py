from PyQt5.QtWidgets import QWidget, QVBoxLayout
from simpleAnalyze.Components.datatable import DataTable

class AnalyzeDataScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.data_table = DataTable()
        layout.addWidget(self.data_table)

        self.setLayout(layout)

    def display_data(self, data):
        self.data_table.update_table(data)


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from simpleAnalyze.Components.datatable import DataTable
from simpleAnalyze.Components.leftPane import LeftPaneWidget

class AnalyzeDataScreen(QWidget):
    def __init__(self):
        super().__init__()


        main_layout = QHBoxLayout(self)


        left_pane = LeftPaneWidget()
        left_pane.setFixedWidth(270)
        main_layout.addWidget(left_pane)


        self.data_table = DataTable()
        main_layout.addWidget(self.data_table)

        self.setLayout(main_layout)


    def display_data(self, data):
        self.data_table.update_table(data)


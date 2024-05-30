from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QAction, QCheckBox
from simpleAnalyze.Components.datatable import DataTable
from simpleAnalyze.Components.leftPane import LeftPaneWidget
from simpleAnalyze.utils.exportmanager import ExportManager

class AnalyzeDataScreen(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        header_layout.addStretch()
        self.export_button = QPushButton("Export")
        self.export_button.setFixedSize(100, 30)
        self.export_button.clicked.connect(self.export_data)
        header_layout.addWidget(self.export_button)

        self.columns_button = QPushButton("Columns")
        self.columns_button.setFixedSize(100, 30)

        menu = QMenu()
        options = ["pid", "process name", "process base", "size", "module name", "module path", "loadtime", "fileoutput"]
        for option in options:
            action = QAction(option, self, checkable=True)
            action.setChecked(True)
            menu.addAction(action)

        self.columns_button.setMenu(menu)

        header_layout.addWidget(self.columns_button)
        main_layout.addLayout(header_layout)

        content_layout = QHBoxLayout()

        left_pane = LeftPaneWidget()
        left_pane.setFixedWidth(270)
        content_layout.addWidget(left_pane)

        self.data_table = DataTable()
        content_layout.addWidget(self.data_table)

        main_layout.addLayout(content_layout)

        self.export_manager = ExportManager()
        self.setLayout(main_layout)

    def display_data(self, data):
        self.data_table.update_table(data)

    def export_data(self):
        data = self.data_table.get_data()
        if data:
            self.export_manager.export_data_as_xml(data, self)

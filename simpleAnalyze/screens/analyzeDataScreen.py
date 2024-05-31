from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from simpleAnalyze.Components.datatable import DataTable
from simpleAnalyze.Components.selectPlugin import SelectPlugin
from simpleAnalyze.Components.selectDump import SelectDump
from simpleAnalyze.Components.runAnalysis import RunAnalysis
from simpleAnalyze.utils.fileUploader import FileUploader

class AnalyzeDataScreen(QWidget):

    def __init__(self, file_uploader, select_plugin, select_dump):
        super().__init__()

        main_layout = QHBoxLayout(self)

        self.select_plugin = select_plugin
        self.file_uploader = file_uploader
        self.select_dump = select_dump
        self.run_analysis = RunAnalysis(self.select_dump, self.select_plugin)
        self.run_analysis.analysis_result.connect(self.display_data)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        self.select_dump.setFixedWidth(270)
        self.select_dump.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        left_layout.addWidget(self.select_dump)

        self.select_plugin.setFixedWidth(270)
        self.select_plugin.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        left_layout.addWidget(self.select_plugin)

        run_button = QPushButton("Run Analysis")
        run_button.setFixedWidth(270)
        run_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        run_button.clicked.connect(self.run_analysis.run_analysis)
        left_layout.addWidget(run_button)

        left_container = QWidget()
        left_container.setLayout(left_layout)
        main_layout.addWidget(left_container, 1)  # Left container takes 25% of the space

        self.data_table = DataTable()
        main_layout.addWidget(self.data_table, 3)  # Data table takes 75% of the space

    def display_data(self, data):
        self.data_table.update_table(data)

    def export_data(self):
        data = self.data_table.get_data()
        if data:
            self.export_manager.export_data_as_xml(data, self)

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QFileDialog
from simpleAnalyze.Components.datatable import DataTable
from simpleAnalyze.Components.columnsSort import ColumnsSort
import xml.etree.ElementTree as ET

class AnalyzeDataScreen(QWidget):

    def __init__(self, file_uploader, select_dump, select_plugin, run_analysis, export_manager):
        super().__init__()

        self.file_uploader = file_uploader
        self.select_dump = select_dump
        self.select_plugin = select_plugin
        self.run_analysis = run_analysis

        main_layout = QHBoxLayout(self)

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

        right_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(7)

        header_layout.addStretch()

        self.columns_sort = ColumnsSort()
        self.columns_sort.setFixedHeight(30)
        self.columns_sort.column_visibility_changed.connect(self.update_column_visibility)
        header_layout.addWidget(self.columns_sort, alignment=Qt.AlignTop)

        self.export_button = QPushButton("Export as...")
        self.export_button.setFixedHeight(30)
        self.export_button.clicked.connect(self.download_as_xml)
        header_layout.addWidget(self.export_button, alignment=Qt.AlignTop)

        right_layout.addLayout(header_layout)

        self.data_table = DataTable()
        self.data_table.headers_updated.connect(self.update_columns_sort)
        right_layout.addWidget(self.data_table)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

    def display_data(self, data):
        self.data_table.update_table(data)

    def download_as_xml(self):
        data = self.data_table.get_data()

        if not data:
            return

        def sanitize_tag(tag):
            return ''.join(c if c.isalnum() or c == '_' else '_' for c in tag)

        root = ET.Element("Data")
        for item in data:
            record = ET.SubElement(root, "Record")
            for key, value in item.items():
                sanitized_key = sanitize_tag(key)
                field = ET.SubElement(record, sanitized_key)
                field.text = str(value)
        tree = ET.ElementTree(root)

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data As", "", "XML Files (*.xml);;All Files (*)",
                                                   options=options)
        if file_name:
            tree.write(file_name, encoding='utf-8', xml_declaration=True)

    def update_column_visibility(self, column_name, is_visible):
        self.data_table.set_column_visibility(column_name, is_visible)

    def update_columns_sort(self, headers):
        self.columns_sort.update_columns(headers)

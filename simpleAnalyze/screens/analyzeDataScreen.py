from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from simpleAnalyze.Components.datatable import DataTable
from simpleAnalyze.Components.leftPane import LeftPaneWidget
import xml.etree.ElementTree as ET

class AnalyzeDataScreen(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout(self)

        left_pane = LeftPaneWidget()
        left_pane.setFixedWidth(270)
        main_layout.addWidget(left_pane)

        data_layout = QVBoxLayout()

        self.export_button = QPushButton("Export as...")
        self.export_button.clicked.connect(self.download_as_xml)
        data_layout.addWidget(self.export_button)

        self.data_table = DataTable()
        data_layout.addWidget(self.data_table)

        main_layout.addLayout(data_layout)

        self.setLayout(main_layout)

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

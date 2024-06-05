import os
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QFileDialog, QLabel, QMainWindow
from PyQt5.uic import  loadUi
import xml.etree.ElementTree as ET


class AnalyzeDataScreen(QMainWindow):

    def __init__(self, active_commands_updated, active_file_path):
        super().__init__()
        loadUi('screens/ui/DataAnalyze.ui', self)

        self.activeCommands = []
        self.activeFilePath = []

        self.output_text = QLabel()
        self.scroll_area_content = QWidget()

        active_file_path.connect(self.update_active_file_path)
        active_commands_updated.connect(self.update_active_commands)

        self.runBtn.clicked.connect(self.run_analysis)

        layout = QVBoxLayout()
        layout.addWidget(self.output_text)
        self.scroll_area_content.setLayout(layout)

        self.dataScroll.setWidget(self.scroll_area_content)

    def update_active_commands(self, active_commands):
        self.activeCommands = active_commands
        print("Active Commands:", self.activeCommands)

    def update_active_file_path(self, active_file_path):
        self.activeFilePath = active_file_path
        print("Active File Path:", self.activeFilePath)

    def run_analysis(self):
        print("Running Analysis")
        command = f"python ../vol.py -f {self.activeFilePath[0]} {self.activeCommands[0]}"
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.output_text.setText(stdout)
            else:
                self.output_text.setText(f"Error: {stderr}")
        except Exception as e:
            print(f'An error occurred: {e}')


        # available buttons:
        # self.checkBoxDump1
        # self.checkBoxDump2
        # self.checkBoxDump3
        # self.checkBoxDump4
        # self.checkBoxPlugin1
        # self.checkBoxPlugin2
        # self.checkBoxPlugin3
        # self.checkBoxPlugin4
        # self.frameFilePlugin
        # self.labelFileText
        # self.labelPluginText
        # self.labelFileChosen
        # self.labelPluginChosen
        # self.labelColumnText
        # self.labelExportText
        # self.labelSearchText
        # self.runBtn


    #     self.file_uploader = file_uploader
    #     self.select_dump = select_dump
    #     self.select_plugin = select_plugin
    #     self.run_analysis = run_analysis
    #
    #     main_layout = QHBoxLayout(self)
    #
    #     # Left layout for select_dump, select_plugin, and run_button
    #     left_layout = QVBoxLayout()
    #     left_layout.setContentsMargins(0, 0, 0, 0)
    #     left_layout.setSpacing(0)
    #
    #     header_layout = QHBoxLayout()
    #
    #     self.select_dump.setFixedWidth(270)
    #     self.select_dump.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    #     left_layout.addWidget(self.select_dump)
    #
    #     self.select_plugin.setFixedWidth(270)
    #     self.select_plugin.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
    #     left_layout.addWidget(self.select_plugin)
    #
    #     self.columns_button = QPushButton("Columns")
    #     self.columns_button.setFixedSize(100, 30)
    #
    #     run_button = QPushButton("Run Analysis")
    #     run_button.setFixedWidth(270)
    #     run_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    #     run_button.clicked.connect(self.run_analysis.run_analysis)
    #     left_layout.addWidget(run_button)
    #
    #     # Right layout for data_table, export_button, and labels
    #     right_layout = QVBoxLayout()
    #
    #     # Layout for labels and export button
    #     labels_and_export_layout = QHBoxLayout()
    #
    #     # Labels for selected file and plugin in a vertical layout
    #     labels_layout = QVBoxLayout()
    #     self.file_label = QLabel("Selected File: None")
    #     self.plugin_label = QLabel("Selected Plugin: None")
    #     labels_layout.addWidget(self.file_label)
    #     labels_layout.addWidget(self.plugin_label)
    #
    #     # Add labels layout to the labels and export layout
    #     labels_and_export_layout.addLayout(labels_layout)
    #
    #     # Export button
    #     self.export_button = QPushButton("Export as...")
    #     self.export_button.clicked.connect(self.download_as_xml)
    #     labels_and_export_layout.addWidget(self.export_button, alignment=Qt.AlignTop | Qt.AlignRight)
    #
    #     right_layout.addLayout(labels_and_export_layout)
    #
    #     self.data_table = DataTable()
    #     right_layout.addWidget(self.data_table)
    #
    #     # Add left and right layouts to main layout
    #     main_layout.addLayout(left_layout)
    #     main_layout.addLayout(right_layout)
    #
    # def update_file_label(self, selected_files):
    #     if selected_files:
    #         self.file_label.setText(f"Selected File: {', '.join([os.path.basename(f) for f in selected_files])}")
    #     else:
    #         self.file_label.setText("Selected File: None")
    #
    # def update_plugin_label(self, plugin_name):
    #     if plugin_name:
    #         self.plugin_label.setText(f"Selected Plugin: {plugin_name}")
    #
    # def display_data(self, data):
    #     self.data_table.update_table(data)
    #
    # def download_as_xml(self):
    #     data = self.data_table.get_data()
    #
    #     if not data:
    #         return
    #
    #     def sanitize_tag(tag):
    #         return ''.join(c if c.isalnum() or c == '_' else '_' for c in tag)
    #
    #     root = ET.Element("Data")
    #     for item in data:
    #         record = ET.SubElement(root, "Record")
    #         for key, value in item.items():
    #             sanitized_key = sanitize_tag(key)
    #             field = ET.SubElement(record, sanitized_key)
    #             field.text = str(value)
    #     tree = ET.ElementTree(root)
    #
    #     options = QFileDialog.Options()
    #     file_name, _ = QFileDialog.getSaveFileName(self, "Save Data As", "", "XML Files (*.xml);;All Files (*)",
    #                                                options=options)
    #     if file_name:
    #         tree.write(file_name, encoding='utf-8', xml_declaration=True)

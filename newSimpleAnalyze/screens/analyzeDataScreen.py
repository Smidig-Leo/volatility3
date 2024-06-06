import os
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QFrame, QFileDialog, QApplication, QHBoxLayout
)
from PyQt5.uic import loadUi
from simpleAnalyze.Components.datatable import DataTable
from simpleAnalyze.Components.columnsSort import ColumnsSort


class AnalyzeDataScreen(QMainWindow):
    """Main window for data analysis."""

    def __init__(self, file_uploader, select_dump, select_plugin, run_analysis):
        """Initialize the AnalyzeDataScreen."""
        super().__init__()
        loadUi('screens/ui/DataAnalyze.ui', self)

        # Load components
        self.file_uploader = file_uploader
        self.select_dump = select_dump
        self.select_plugin = select_plugin
        self.run_analysis = run_analysis
        self.data_table = DataTable()
        self.columns_sort = ColumnsSort()

        # Set initial values
        self.labelFileChosen.setText("None")
        self.labelPluginChosen.setText("None")

        # Find frames
        self.frameDumps = self.findChild(QFrame, 'frameDumps')
        self.framePluginContent = self.findChild(QFrame, 'framePluginContent')
        self.frameDataContent = self.findChild(QFrame, 'frame_7')
        self.dataScroll = self.findChild(QFrame, 'dataScroll')
        self.frame = self.findChild(QFrame, 'frame')
        self.runBtn = self.findChild(QPushButton, 'runBtn')
        self.frameTopRight = self.findChild(QFrame, 'frame_10')
        self.pluginsParentFrame = self.findChild(QFrame, 'frame_11')

        # Add export button
        self.export_button = QPushButton("Export as...")
        self.export_button.setFixedHeight(30)
        self.export_button.clicked.connect(self.download_as_xml)
        self.frameTopRight.layout().addWidget(self.export_button)

        # Data Table
        data_layout = QHBoxLayout()
        self.dataScroll.setLayout(data_layout)
        data_layout.addWidget(self.data_table)

        # Columns sort
        self.columns_sort.setFixedHeight(30)
        self.columns_sort.column_visibility_changed.connect(self.update_column_visibility)
        self.frameTopRight.layout().addWidget(self.columns_sort)

        # Retrieve existing layouts
        dump_layout = self.frameDumps.layout()
        plugin_layout = self.framePluginContent.layout()
        dump_layout.addWidget(self.select_dump)
        plugin_layout.addWidget(self.select_plugin)

        # Connect signals
        self.data_table.headers_updated.connect(self.update_columns_sort)
        self.runBtn.clicked.connect(self.start_analysis)

        # Set the width of frames
        self.set_frame_width()

    def set_frame_width(self):
        """Set the width of frames to 20% of the screen width."""
        screen_width = QApplication.desktop().screenGeometry().width()
        frame_width = int(0.15 * screen_width)
        for frame in [self.frameDumps, self.frame, self.framePluginContent]:
            frame.setFixedWidth(frame_width)

    def update_file_label(self, selected_files):
        """Update the file label with selected files."""
        if selected_files:
            file_names = [os.path.basename(file[0]) for file in selected_files]
            self.labelFileChosen.setText(", ".join(file_names))

    def update_plugin_label(self, plugin_name):
        """Update the plugin label."""
        self.labelPluginChosen.setText(plugin_name)

    def display_data(self, data):
        """Display data in the data table."""
        self.data_table.update_table(data)

    def download_as_xml(self):
        """Export data as XML."""
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
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Data As", "", "XML Files (*.xml);;All Files (*)",
            options=options
        )
        if file_name:
            tree.write(file_name, encoding='utf-8', xml_declaration=True)

    def update_column_visibility(self, column_name, is_visible):
        """Update column visibility."""
        self.data_table.set_column_visibility(column_name, is_visible)

    def update_columns_sort(self, headers):
        """Update column sorting."""
        self.columns_sort.update_columns(headers)

    def start_analysis(self):
        """Start data analysis."""
        self.run_analysis.run_analysis()


'''     self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 100)
        self.loading_bar.setValue(0)
        right_layout.addWidget(self.loading_bar)

        self.reset_timer = QTimer(self)
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.reset_progress_bar)

        self.original_button_text = self.runBtn.text()'''



'''    def start_analysis(self):
        self.loading_bar.setValue(0)  # Reset loading bar
        self.update_button_text("Analyzing...")  # Update button text
        self.run_analysis.progress_updated.connect(self.update_progress)
        self.run_analysis.analysis_result.connect(self.analysis_complete)  # Connect analysis_complete slot
        self.run_analysis.run_analysis()'''



'''    def update_progress(self, progress_percentage):
        self.loading_bar.setValue(progress_percentage)

    def analysis_complete(self):
        self.reset_timer.start(3000)
        self.update_button_text(self.original_button_text)

    def reset_progress_bar(self):
        self.loading_bar.setValue(0)

    def update_button_text(self, text):
        self.runBtn.setText(text)
'''


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


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QCheckBox, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
import subprocess
from simpleAnalyze.data.plugins.pluginManager import PluginManager

class PluginScreen(QWidget):
    plugins_updated = pyqtSignal(list)

    def __init__(self, plugin_manager):
        super().__init__()
        self.plugins = []
        self.file_path = ""
        self.selected_plugins = []
        self.plugin_manager = plugin_manager
        self.search_text = ""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search Plugins")
        self.search_bar.textChanged.connect(self.filter_plugins)
        self.layout.addWidget(self.search_bar)
        os_type = "windows"
        self.load_plugins(os_type)

    def load_plugins(self, os_type):
        self.plugins = self.plugin_manager.get_plugins(os_type)
        self.clear_layout()
        self.populate_plugin_checkboxes()
        self.plugins_updated.emit([plugin.name for plugin in self.plugins])



    def populate_plugin_checkboxes(self):
        filtered_plugins = [plugin for plugin in self.plugins if self.search_text.lower() in plugin.name.lower()]
        for plugin in filtered_plugins:
            checkbox = QCheckBox(plugin.name)
            checkbox.clicked.connect(self.toggle_plugin)
            checkbox.setChecked(True)
            self.layout.addWidget(checkbox)

    def toggle_plugin(self):
        self.selected_plugins = [checkbox.text() for checkbox in self.findChildren(QCheckBox) if checkbox.isChecked()]
        self.plugins_updated.emit(self.selected_plugins)

    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

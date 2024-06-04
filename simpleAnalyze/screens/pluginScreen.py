from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QCheckBox
from PyQt5.QtCore import pyqtSignal
import subprocess
from simpleAnalyze.data.plugins.pluginManager import PluginManager

class PluginScreen(QWidget):
    plugins_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.selected_plugins = []
        self.plugin_manager = PluginManager()
        self.selected_os = "windows"

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.load_plugins(self.selected_os)

    def load_plugins(self, os):
        self.plugin_manager.load_plugins(os, self.file_path)
        self.plugins = self.plugin_manager.get_plugins()
        self.populate_plugin_checkboxes()

    def populate_plugin_checkboxes(self):

        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for plugin in self.plugins:
            checkbox = QCheckBox(plugin.name)
            checkbox.stateChanged.connect(self.toggle_plugin)
            self.layout.addWidget(checkbox)
            if self.selected_os in self.selected_plugins and plugin.name in self.selected_plugins[self.selected_os]:
                checkbox.setChecked(True)
            self.layout.addWidget(checkbox)

    def set_os(self, os):
        self.selected_os = str(os)
        print("OS set to ", self.selected_os)
        self.load_plugins(self.selected_os)

    def toggle_plugin(self):
        plugin_name = self.sender().text()
        if self.file_path:
            if plugin_name in self.selected_plugins:
                self.selected_plugins.remove(plugin_name)
                self.sender().setStyleSheet("")
            else:
                self.selected_plugins.append(plugin_name)


            self.plugins_updated.emit(self.selected_plugins)

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.load_plugins(self.selected_os)

    def clear_file_path(self):
        self.file_path = ""
        self.selected_plugins.clear()
        self.load_plugins(self.selected_os)

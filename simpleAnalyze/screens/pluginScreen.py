from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QCheckBox, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt

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
        self.setup_search_bar()
        os_type = "windows"
        self.load_plugins(os_type)

    def setup_search_bar(self):
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Plugins")
        search_layout.addWidget(self.search_bar)
        search_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(search_layout)
        self.search_bar.textChanged.connect(self.populate_plugin_checkboxes)  # Connect to the method for filtering

    def load_plugins(self, os_type):
        self.plugins = self.plugin_manager.get_plugins(os_type)
        self.clear_layout()
        self.populate_plugin_checkboxes()
        self.plugins_updated.emit([plugin.name for plugin in self.plugins])

    def populate_plugin_checkboxes(self):
        self.clear_layout()  # Clear existing checkboxes
        self.search_text = self.search_bar.text()
        for plugin in self.plugins:
            if self.search_text.lower() in plugin.name.lower():
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

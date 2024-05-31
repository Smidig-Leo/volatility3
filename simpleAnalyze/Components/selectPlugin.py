from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from simpleAnalyze.data.plugins.pluginManager import PluginManager

class SelectPlugin(QWidget):
    plugin_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.selected_os = "windows"
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins(self.selected_os, self.file_path)
        self.plugins_group = QGroupBox("PLUGINS")
        self.plugins_layout = QVBoxLayout()
        self.plugins_header = QLabel("PLUGINS")
        self.plugins_subheader = QLabel("Choose a plugin to analyze memory dump")
        self.plugins_list = QListWidget()
        self.populate_plugins_list()
        self.apply_styles()

        # Add widgets to the layout
        self.plugins_layout.addWidget(self.plugins_header)
        self.plugins_layout.addWidget(self.plugins_subheader)
        self.plugins_layout.addWidget(self.plugins_list)
        self.plugins_group.setLayout(self.plugins_layout)

        # Set the layout of the SelectPlugin widget to the layout of the QGroupBox
        self.setLayout(self.plugins_group.layout())

    def populate_plugins_list(self):
        # change this to get activated plugins
        plugins = self.plugin_manager.get_plugins()
        for plugin in plugins:
            item = QListWidgetItem(plugin.name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, plugin)
            self.plugins_list.addItem(item)
            self.plugins_list.itemChanged.connect(self.plugin_selection_changed)

    def plugin_selection_changed(self, item):
        if item.checkState() == Qt.Checked:
            selected_plugin = item.data(Qt.UserRole)
            self.plugin_selected.emit(selected_plugin.name)
            if selected_plugin:
                for index in range(self.plugins_list.count()):
                    if self.plugins_list.item(index) is not item:
                        self.plugins_list.item(index).setCheckState(Qt.Unchecked)

    def apply_styles(self):
        # Apply styles to QLabel
        self.plugins_header.setStyleSheet("""
            color:#FFFFFF;
            font-size: 18px;
            padding: 0px;
            border: none;
            border-bottom: 1px solid #F27821;
        """)
        self.plugins_subheader.setStyleSheet("""
            color: #FFFFFF;
            font-size: 9px;
        """)

        # Apply styles to QListWidget
        self.plugins_list.setStyleSheet("""
            QListWidget {
                border-radius: 5px;
                background-color: #343534;
                color: white;
                border: none;
                padding: 0px;
            }

            QListWidget::item {
                color: white;
                height: 25px;
                padding: 0px;
                border: none;
                border-bottom: 1px solid #ccc;
                background-color: #343534;
            }

            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }

            QListWidget::item::indicator {
                width: 20px;
                height: 20px;
            }
        """)


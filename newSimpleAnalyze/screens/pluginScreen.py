from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMainWindow, QFrame, QHBoxLayout, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.uic import loadUi
from newSimpleAnalyze.Components.py_toggle import PyToggle
from newSimpleAnalyze.data.plugins.pluginManager import PluginManager

class PluginScreen(QMainWindow):
    plugins_updated = pyqtSignal(list)
    activeCommandsUpdated = pyqtSignal(list)

    def __init__(self, session_manager):
        super().__init__()
        loadUi('screens/ui/Plugins.ui', self)

        self.session_manager = session_manager
        self.activeCommands = self.session_manager.get_activated_plugins()

        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(0)

        self.pluginScroll.setLayout(scroll_layout)

        widget = QWidget()
        widget.setLayout(scroll_layout)

        self.pluginScroll.setWidget(widget)

        self.plugins_data = PluginManager()
        self.search_bar = self.findChild(QLineEdit, 'lineEditPluginSearch')
        if self.search_bar is None:
            raise ValueError("Could not find the search bar widget. Please check the object name in the .ui file.")
        self.search_bar.setPlaceholderText("Search Plugins")
        self.search_bar.textChanged.connect(lambda: self.populate_plugin_toggles(scroll_layout))

        self.plugins = self.plugins_data.get_plugins('windows')
        self.populate_plugin_toggles(scroll_layout)

    def create_plugin_toggle(self, scroll_layout, plugin_name, color):
        firstFrame = QFrame()
        secondFrame = QFrame()
        thirdFrame = QFrame()

        primaryColor = "background-color:rgb(38, 38, 38);"
        secondaryColor = "background-color:rgb(52, 53, 52);"

        if color == "primary":
            firstFrame.setStyleSheet(primaryColor)
        elif color == "secondary":
            firstFrame.setStyleSheet(secondaryColor)

        firstFrame.setMaximumHeight(100)

        layout = QHBoxLayout()
        layout.addWidget(secondFrame)
        layout.addWidget(thirdFrame)

        firstFrame.setLayout(layout)

        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        label1 = QLabel(plugin_name)
        label1.setStyleSheet("color:white;")
        layout2.addWidget(label1)

        toggle = PyToggle()
        layout3.addWidget(toggle)
        layout3.setAlignment(toggle, Qt.AlignRight)

        secondFrame.setLayout(layout2)
        thirdFrame.setLayout(layout3)

        toggle.setChecked(plugin_name in self.activeCommands)
        toggle.stateChanged.connect(lambda: self.setActiveCommands(plugin_name, toggle.isChecked()))

        scroll_layout.addWidget(firstFrame)

    def setActiveCommands(self, plugin_name, isChecked):
        if isChecked:
            self.activeCommands.append(plugin_name)
        else:
            self.activeCommands.remove(plugin_name)
        print(f"Plugin '{plugin_name}' toggled to {'ON' if isChecked else 'OFF'}")
        print(f"Active Commands: {self.activeCommands}")
        self.activeCommandsUpdated.emit(self.activeCommands)
        self.plugins_updated.emit(self.activeCommands)
        self.session_manager.set_activated_plugins(self.activeCommands)

    def populate_plugin_toggles(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QFrame):
                widget.deleteLater()

        search_text = self.search_bar.text().lower()

        for i, plugin in enumerate(self.plugins):
            if search_text in plugin.name.lower():
                color = "secondary" if (i + 1) % 2 == 0 else "primary"
                self.create_plugin_toggle(layout, plugin.name, color)
    #     self.file_path = ""
    #     self.selected_plugins = []
    #     self.plugin_manager = PluginManager()
    #     self.selected_os = "windows"
    #
    #     self.layout = QVBoxLayout()
    #     self.setLayout(self.layout)
    #
    #     self.load_plugins(self.selected_os)
    #
    # def load_plugins(self, os):
    #     self.plugin_manager.load_plugins(os, self.file_path)
    #     self.plugins = self.plugin_manager.get_plugins()
    #     self.populate_plugin_checkboxes()
    #
    # def populate_plugin_checkboxes(self):
    #
    #     for i in reversed(range(self.layout.count())):
    #         widget = self.layout.itemAt(i).widget()
    #         if widget:
    #             widget.deleteLater()
    #
    #     for plugin in self.plugins:
    #         checkbox = QCheckBox(plugin.name)
    #         checkbox.stateChanged.connect(self.toggle_plugin)
    #         self.layout.addWidget(checkbox)
    #         if self.selected_os in self.selected_plugins and plugin.name in self.selected_plugins[self.selected_os]:
    #             checkbox.setChecked(True)
    #         self.layout.addWidget(checkbox)
    #
    # def set_os(self, os):
    #     self.selected_os = str(os)
    #     print("OS set to ", self.selected_os)
    #     self.load_plugins(self.selected_os)
    #
    # def toggle_plugin(self):
    #     plugin_name = self.sender().text()
    #     if self.file_path:
    #         if plugin_name in self.selected_plugins:
    #             self.selected_plugins.remove(plugin_name)
    #             self.sender().setStyleSheet("")
    #         else:
    #             self.selected_plugins.append(plugin_name)
    #
    #
    #         self.plugins_updated.emit(self.selected_plugins)
    #
    # def set_file_path(self, file_path):
    #     self.file_path = file_path
    #     self.load_plugins(self.selected_os)
    #
    # def clear_file_path(self):
    #     self.file_path = ""
    #     self.selected_plugins.clear()
    #     self.load_plugins(self.selected_os)

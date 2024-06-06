from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QCheckBox, QMainWindow, QFrame, \
    QHBoxLayout, QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from newSimpleAnalyze.Components.py_toggle import PyToggle
from newSimpleAnalyze.data.plugins.pluginManager import PluginManager
import subprocess

class PluginScreen(QMainWindow):
    plugins_updated = pyqtSignal(list)
    activeCommandsUpdated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        loadUi('screens/ui/Plugins.ui', self)

        #All buttons made in code none in .ui

        self.activeCommands = []

        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(0)

        self.pluginScroll.setLayout(scroll_layout)

        widget = QWidget()
        widget.setLayout(scroll_layout)

        self.pluginScroll.setWidget(widget)

        self.plugins_data = PluginManager()
        # Connect the existing search bar from the .ui file
        self.search_bar = self.findChild(QLineEdit,'lineEditPluginSearch')  # Ensure 'lineEditPluginSearch' matches the object name in the .ui file
        if self.search_bar is None:
            raise ValueError("Could not find the search bar widget. Please check the object name in the .ui file.")
        self.search_bar.setPlaceholderText("Search Plugins")
        self.search_bar.textChanged.connect(lambda: self.populate_plugin_checkboxes(scroll_layout))

        self.plugins = self.plugins_data.get_plugins('windows')
        self.populate_plugin_checkboxes(scroll_layout)



        for i in range(len(self.plugins_data.get_plugins('windows'))):
            plugin = self.plugins_data.get_plugins('windows')[i]

            if (i+1) % 2 == 0:
                self.create_plugins(scroll_layout, plugin.get_name(), "secondary")
            else:
                self.create_plugins(scroll_layout, plugin.get_name(), "primary")

    def create_plugins(self, scroll_layout, command, color):
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

        label1 = QLabel(command)
        label1.setStyleSheet("color:white;")
        layout2.addWidget(label1)

        toggle = PyToggle()
        layout3.addWidget(toggle)
        layout3.setAlignment(toggle, Qt.AlignRight)

        secondFrame.setLayout(layout2)
        thirdFrame.setLayout(layout3)

        toggle.stateChanged.connect(lambda: self.setActiveCommands(command, toggle.isChecked()))

        scroll_layout.addWidget(firstFrame)

        # self.label = QLabel("Test")
        #
        # self.layout().addWidget(self.label)

    def setActiveCommands(self, command, isChecked):
        if isChecked:
            self.activeCommands.append(command)
        else:
            self.activeCommands.remove(command)
        self.activeCommandsUpdated.emit(self.activeCommands)

    def populate_plugin_checkboxes(self, layout):
        # Clear current plugin checkboxes
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QFrame):
                widget.deleteLater()

        search_text = self.search_bar.text().lower()

        for i, plugin in enumerate(self.plugins):
            if search_text in plugin.name.lower():
                color = "secondary" if (i + 1) % 2 == 0 else "primary"
                self.create_plugins(layout, plugin.name, color)
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

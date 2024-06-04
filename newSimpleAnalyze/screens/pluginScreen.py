from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QCheckBox, QMainWindow, QFrame, \
    QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from newSimpleAnalyze.Components.py_toggle import PyToggle
import subprocess

class PluginScreen(QMainWindow):
    plugins_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        loadUi('screens/ui/Plugins.ui', self)
        scroll_layout = QVBoxLayout()

        # Add the layout to pluginScroll
        self.pluginScroll.setLayout(scroll_layout)

        # Create a widget to hold all the frames
        widget = QWidget()
        widget.setLayout(scroll_layout)

        # Set the widget as the scroll area's widget
        self.pluginScroll.setWidget(widget)

        for i in range(20):
            self.create_plugins(scroll_layout)

    def create_plugins(self, scroll_layout):
        firstFrame = QFrame()
        secondFrame = QFrame()
        thirdFrame = QFrame()

        firstFrame.setStyleSheet("background-color:rgb(38, 38, 38);")
        firstFrame.setMaximumHeight(100)

        # Create a QHBoxLayout
        layout = QHBoxLayout()

        layout.addWidget(secondFrame)
        layout.addWidget(thirdFrame)

        firstFrame.setLayout(layout)

        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        label1 = QLabel("windows.pslist")
        label1.setStyleSheet("color:white;")
        layout2.addWidget(label1)

        toggle = PyToggle()
        layout3.addWidget(toggle)
        layout3.setAlignment(toggle, Qt.AlignRight)

        secondFrame.setLayout(layout2)
        thirdFrame.setLayout(layout3)

        # Add firstFrame to the scroll_layout
        scroll_layout.addWidget(firstFrame)



        # self.label = QLabel("Test")
        #
        # self.layout().addWidget(self.label)

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

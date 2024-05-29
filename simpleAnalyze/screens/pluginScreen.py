from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
import subprocess
from simpleAnalyze.data.plugins.pluginManager import PluginManager


class PluginScreen(QWidget):
    analysis_result = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.selected_plugins = []
        self.plugin_manager = PluginManager()
        self.selected_os = "windows"

        self.layout = QVBoxLayout()

        self.file_label = QLabel("No memory dump selected")
        self.layout.addWidget(self.file_label)

        # Load plugins for a specific OS (e.g., "windows")
        self.plugin_manager.load_plugins(self.selected_os, self.file_path)
        self.plugins = self.plugin_manager.get_plugins()

        self.plugin_manager.load_plugins(self.selected_os, self.file_path)
        self.plugins = self.plugin_manager.get_plugins()

        for plugin in self.plugins:
            btn = QPushButton(plugin.name)
            btn.clicked.connect(self.toggle_plugin)
            self.layout.addWidget(btn)

        self.run_button = QPushButton("Run Analysis")
        self.run_button.clicked.connect(self.run_analysis)
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)

    def set_os(self, os):
        self.selected_os = str(os)
        print("OS hitt ", self.selected_os)
        self.refresh_buttons()

    def refresh_buttons(self):
        self.plugin_manager.load_plugins(self.selected_os, self.file_path)
        self.plugins = self.plugin_manager.get_plugins()

        for i in reversed(range(1, self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.deleteLater()

        for plugin in self.plugins:
            btn = QPushButton(plugin.name)
            btn.clicked.connect(self.toggle_plugin)
            self.layout.addWidget(btn)

        new_run_button = QPushButton("Run Analysis")
        new_run_button.clicked.connect(self.run_analysis)
        self.layout.addWidget(new_run_button)

        self.layout.update()


    def toggle_plugin(self):
        plugin_name = self.sender().text()
        if self.file_path:
            if plugin_name in self.selected_plugins:
                self.selected_plugins.remove(plugin_name)
                self.sender().setStyleSheet("")
            else:
                self.selected_plugins.append(plugin_name)
                self.sender().setStyleSheet("background-color: green;")
        else:
            QMessageBox.critical(self, "Error", "No memory dump selected")

    def run_analysis(self):
        if self.file_path:
            output_text = ""
            for plugin in self.selected_plugins:
                for p in self.plugins:
                    if p.name == plugin:
                        try:
                            result = subprocess.Popen(p.command.format(file_path=self.file_path, name=p.name),
                                                      shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                      text=True)
                            stdout, stderr = result.communicate()
                            if result.returncode == 0:
                                output_text += f"{p.name}: {stdout}\n"
                        except Exception as e:
                            print(f'An error occurred: {e}')
            self.analysis_result.emit(output_text)
        else:
            QMessageBox.critical(self, "Error", "No memory dump selected")

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.file_label.setText(f"Selected file: {self.file_path}")
        self.plugin_manager.load_plugins("windows", self.file_path)

    def clear_file_path(self):
        self.file_path = ""
        self.file_label.setText("No memory dump selected")
        self.selected_plugins.clear()
        self.refresh_buttons()

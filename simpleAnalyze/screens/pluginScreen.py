from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
import subprocess
class PluginScreen(QWidget):
    analysis_result = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.selected_plugins = []

        layout = QVBoxLayout()

        self.file_label = QLabel("No memory dump selected")
        layout.addWidget(self.file_label)

        self.plugins = ["windows.pslist", "windows.cmdline", "windows.dlllist", "windows.info"]

        for plugin in self.plugins:
            btn = QPushButton(plugin)
            btn.clicked.connect(self.toggle_plugin)
            layout.addWidget(btn)

        self.run_button = QPushButton("Run Analysis")
        self.run_button.clicked.connect(self.run_analysis)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

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
                cmd = f"python ../vol.py -f {self.file_path} {plugin}"
                try:
                    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                              text=True)
                    stdout, stderr = result.communicate()
                    if result.returncode == 0:
                        output_text += f"{plugin}: {stdout}\n"
                except Exception as e:
                    print(f'An error occured: {e}')
            self.analysis_result.emit(output_text)
        else:
            QMessageBox.critical(self, "Error", "No memory dump selected")

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.file_label.setText(f"Selected file: {self.file_path}")
import subprocess
from PyQt5.QtCore import pyqtSignal, QObject

class RunAnalysis(QObject):
    analysis_result = pyqtSignal(str)

    def __init__(self, select_dump, select_plugin):
        super().__init__()
        self.plugin = ""
        self.selected_files = []
        self.select_dump = select_dump
        self.select_plugin = select_plugin
        self.select_dump.file_selected.connect(self.handle_selected_files)
        self.select_plugin.plugin_selected.connect(self.handle_selected_plugin)

    def handle_selected_plugin(self, selected_plugin):
        self.plugin = selected_plugin

    def handle_selected_files(self, selected_files):
        self.selected_files = selected_files

    def run_analysis(self):
        if self.selected_files and self.plugin:
            try:
                for files in self.selected_files:
                    command = ["python", "../vol.py", "-f", files, self.plugin]
                    print(f"Running command: {' '.join(command)}")  # Debugging statement
                    output = subprocess.check_output(command)
                    self.analysis_result.emit(output.decode())
            except subprocess.CalledProcessError as e:
                # Emit an error message signal
                self.analysis_result.emit("Error: " + e.output.decode())
        else:
            # Emit an error message signal
            self.analysis_result.emit("Error: No plugin or memory dump selected")

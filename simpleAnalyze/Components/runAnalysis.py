import subprocess
from PyQt5.QtCore import pyqtSignal, QObject


class RunAnalysis(QObject):
    analysis_result = pyqtSignal(str)

    def __init__(self, select_dump, select_plugin):
        super().__init__()
        self.plugin = []
        self.selected_files = []
        self.select_dump = select_dump
        self.select_plugin = select_plugin
        self.select_plugin.plugin_selected.connect(self.handle_selected_plugin)

    def handle_selected_plugin(self, selected_plugin):
        self.plugin = selected_plugin

    def handle_selected_files(self, selected_files):
        self.selected_files = selected_files
        print("Selected files: ", self.selected_files)

    def run_analysis(self):
        if self.selected_files and self.plugin:
            try:
                summary = ""
                first_file = True  # Flag to check if it's the first file
                for file in self.selected_files:
                    command = ["python", "../vol.py", "-f", file, self.plugin]
                    print(f"Running command: {' '.join(command)}")  # Debugging statement
                    output = subprocess.check_output(command).decode()

                    # Split output into lines
                    lines = output.splitlines()

                    if first_file:
                        # Include the entire output including headers for the first file
                        summary += "\n".join(lines)
                        first_file = False
                    else:
                        # Exclude the headers (assuming headers are in the first few lines)
                        data_lines = lines[3:]  # Adjust index if headers span more lines
                        summary += "\n" + "\n".join(data_lines)

                self.analysis_result.emit(summary)
            except subprocess.CalledProcessError as e:
                # Emit an error message signal
                self.analysis_result.emit("Error: " + e.output.decode())
        else:
            # Emit an error message signal
            self.analysis_result.emit("Error: No plugin or memory dump selected")
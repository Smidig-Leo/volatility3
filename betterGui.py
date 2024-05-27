import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox
import subprocess

class SelectFileScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.file_label = QLabel("No memory dump selected")
        layout.addWidget(self.file_label)

        self.select_button = QPushButton("Select Memory Dump")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"Selected file: {self.file_path}")
            self.parent().plugin_screen.file_path = self.file_path
            self.parent().plugin_screen.file_label.setText(f"Selected file: {self.file_path}")


class PluginScreen(QWidget):
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
        if plugin_name in self.selected_plugins:
            self.selected_plugins.remove(plugin_name)
            self.sender().setStyleSheet("")
        else:
            self.selected_plugins.append(plugin_name)
            self.sender().setStyleSheet("background-color: green;")

    def run_analysis(self):
        if self.file_path:
            output_text = ""
            for plugin in self.selected_plugins:
                cmd = f"python vol.py -f {self.file_path} {plugin}"
                try:
                    result = subprocess.Popen(cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = result.communicate()
                    if result.returncode == 0:
                        output_text += f"{plugin}: {stdout}\n"
                        self.parent().analyzed_data_screen.output_text.setPlainText(output_text)
                        self.parent().setCurrentIndex(2)
                except Exception as e:
                    print(f'An error occured: {e}')

#                output_text += f"Output for {plugin}:\n{result.stdout}\n{'=' * 40}\n"

        else:
            QMessageBox.critical(self, "Error", "No memory dump selected")


class AnalyzedDataScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.output_text = QTextEdit()
        layout.addWidget(self.output_text)

        self.setLayout(layout)


class VolatilityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volatility App")
        self.setGeometry(100, 100, 800, 600)

        self.select_file_screen = SelectFileScreen()
        self.plugin_screen = PluginScreen()
        self.analyzed_data_screen = AnalyzedDataScreen()

        self.setCentralWidget(self.select_file_screen)

        select_file_action = QPushButton("Select File")
        select_file_action.clicked.connect(self.show_select_file_screen)

        plugins_action = QPushButton("Plugins")
        plugins_action.clicked.connect(self.show_plugin_screen)

        analyzed_data_action = QPushButton("Analyzed Data")
        analyzed_data_action.clicked.connect(self.show_analyzed_data_screen)

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.addWidget(select_file_action)
        self.toolbar.addWidget(plugins_action)
        self.toolbar.addWidget(analyzed_data_action)

    def show_select_file_screen(self):
        self.setCentralWidget(self.select_file_screen)

    def show_plugin_screen(self):
        self.setCentralWidget(self.plugin_screen)

    def show_analyzed_data_screen(self):
        self.setCentralWidget(self.analyzed_data_screen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VolatilityApp()
    window.show()
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QStackedWidget
import subprocess
from PyQt5.QtCore import QObject, pyqtSignal
from uploadConfirmation import is_valid_memory_dump, is_file_exists

class SelectFileScreen(QWidget):
    file_path_set = pyqtSignal(str)
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
            if is_valid_memory_dump(file_path) and is_file_exists(file_path):
                self.file_path = file_path
                self.file_label.setText(f"Selected file: {self.file_path}")
                self.file_path_set.emit(file_path)
            else:
                QMessageBox.critical(self, "Error", "The file you selected is not a valid memory dump! Please select a valid file.\n(Supported file extensions: .vmem)")

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
            print(self.file_path)
            output_text = ""
            for plugin in self.selected_plugins:
                cmd = f"python vol.py -f {self.file_path} {plugin}"
                try:
                    result = subprocess.Popen(cmd, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = result.communicate()
                    if result.returncode == 0:
                        output_text += f"{plugin}: {stdout}\n"
                        #self.parent().analyzed_data_screen.output_text.setPlainText(output_text)
                except Exception as e:
                    print(f'An error occured: {e}')
            self.analysis_result.emit(output_text)
        else:
            QMessageBox.critical(self, "Error", "No memory dump selected")

    def set_file_path(self, file_path):
        print(file_path)
        self.file_path = file_path
        self.file_label.setText(f"Selected file: {self.file_path}")


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

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.stacked_widget.addWidget(self.select_file_screen)
        self.stacked_widget.addWidget(self.plugin_screen)
        self.stacked_widget.addWidget(self.analyzed_data_screen)

        self.select_file_screen.file_path_set.connect(self.plugin_screen.set_file_path)
        self.plugin_screen.analysis_result.connect(self.update_analyzed_data)

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
        self.stacked_widget.setCurrentWidget(self.select_file_screen)

    def show_plugin_screen(self):
        self.stacked_widget.setCurrentWidget(self.plugin_screen)

    def show_analyzed_data_screen(self):
        self.stacked_widget.setCurrentWidget(self.analyzed_data_screen)

    def update_analyzed_data(self, analyzed_result):
        self.analyzed_data_screen.output_text.setPlainText(analyzed_result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VolatilityApp()
    window.show()
    sys.exit(app.exec_())
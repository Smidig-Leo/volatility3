import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton
from screens.mainPage import MainPage
from screens.pluginScreen import PluginScreen
from screens.analyzeDataScreen import AnalyzeDataScreen
from screens.settingsPage import SettingsPage
from data.sessionManager import SessionManager
from Components.selectDump import SelectDump
from Components.runAnalysis import RunAnalysis
from Components.selectPlugin import SelectPlugin
from utils.fileUploader import FileUploader
from utils.chooseOs import ChooseOs



class VolatilityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volatility App")
        self.setGeometry(100, 100, 800, 600)

        # Initialize session manager to store user state
        self.session_manager = SessionManager()
        self.session_manager.load_session()
        self.select_dump = SelectDump()
        self.chooseOs = ChooseOs()
        self.select_plugin = SelectPlugin()
        self.file_uploader = FileUploader(self)
        self.run_analysis = RunAnalysis(self.select_dump, self.select_plugin)

        self.select_file_screen = MainPage(self, self.file_uploader, self.chooseOs)
        self.plugin_screen = PluginScreen()
        self.analyzed_data_screen = AnalyzeDataScreen(select_dump=self.select_dump, select_plugin=self.select_plugin, file_uploader=self.file_uploader, run_analysis=self.run_analysis, export_manager=None)
        self.file_uploader.file_path_updated.connect(self.select_dump.update_file_paths)
        self.settings_screen = SettingsPage()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.stacked_widget.addWidget(self.select_file_screen)
        self.stacked_widget.addWidget(self.plugin_screen)
        self.stacked_widget.addWidget(self.analyzed_data_screen)
        self.stacked_widget.addWidget(self.settings_screen)

        self.select_file_screen.os_selected.connect(self.plugin_screen.set_os)
        self.select_file_screen.file_path_set.connect(self.plugin_screen.set_file_path)
        self.plugin_screen.analysis_result.connect(self.update_analyzed_data)

        select_file_action = QPushButton("Select File")
        select_file_action.clicked.connect(self.show_select_file_screen)

        plugins_action = QPushButton("Plugins")
        plugins_action.clicked.connect(self.show_plugin_screen)

        analyzed_data_action = QPushButton("Analyzed Data")
        analyzed_data_action.clicked.connect(self.show_analyzed_data_screen)

        settings_action = QPushButton("Settings")
        settings_action.clicked.connect(self.show_settings_screen)

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.addWidget(select_file_action)
        self.toolbar.addWidget(plugins_action)
        self.toolbar.addWidget(analyzed_data_action)
        self.toolbar.addWidget(settings_action)

        # Setup connections for the run analysis process
        self.select_plugin.plugin_selected.connect(self.run_analysis.handle_selected_plugin)
        self.run_analysis.analysis_result.connect(self.analyzed_data_screen.display_data)

        # Set the files uploaded from previous session
        file_paths = self.session_manager.get_file_uploaded()
        if file_paths:
            for file_path in file_paths:
                self.select_file_screen.file_uploader.add_file_path(file_path)
                self.plugin_screen.set_file_path(file_path)

        # Connect the file uploader signal to update file paths in SelectDump
        self.file_uploader.file_path_updated.connect(self.select_dump.update_file_paths)

    def show_select_file_screen(self):
        self.stacked_widget.setCurrentWidget(self.select_file_screen)

    def show_plugin_screen(self):
        self.stacked_widget.setCurrentWidget(self.plugin_screen)

    def show_analyzed_data_screen(self):
        self.stacked_widget.setCurrentWidget(self.analyzed_data_screen)

    def show_settings_screen(self):
        self.stacked_widget.setCurrentWidget(self.settings_screen)

    def update_analyzed_data(self, analyzed_result):
        self.analyzed_data_screen.display_data(analyzed_result)

    def closeEvent(self, event):
        self.session_manager.save_session()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VolatilityApp()
    window.show()
    sys.exit(app.exec_())

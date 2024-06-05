import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton
from screens.mainPage import MainPage
from screens.analyzeDataScreen import AnalyzeDataScreen
from screens.pluginScreen import PluginScreen
from screens.settingsPage import SettingsPage
from PyQt5.uic import loadUi




class VolatilityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('screens/ui/NavigationBar.ui', self)
        self.setWindowTitle("Volatility3")

        # NavBar available buttons:
        # self.mainBtn
        # self.dataBtn
        # self.pluginsBtn
        # self.settingsBtn

        self.main_page = MainPage()
        self.data_page = AnalyzeDataScreen()
        self.plugins_page = PluginScreen()
        self.settings_page = SettingsPage()

        self.stackedWidget.addWidget(self.main_page)
        self.stackedWidget.addWidget(self.data_page)
        self.stackedWidget.addWidget(self.plugins_page)
        self.stackedWidget.addWidget(self.settings_page)

        self.mainBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.main_page))
        self.dataBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.data_page))
        self.pluginsBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.plugins_page))
        self.settingsBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.settings_page))



    #     # Setup connections for the run analysis process
    #     self.select_plugin.plugin_selected.connect(self.run_analysis.handle_selected_plugin)
    #     self.run_analysis.analysis_result.connect(self.analyzed_data_screen.display_data)
    #
    #     # Set the files uploaded from previous session
    #     file_paths = self.session_manager.get_file_uploaded()
    #     if file_paths:
    #         for file_path in file_paths:
    #             self.select_file_screen.file_uploader.add_file_path(file_path)
    #             self.plugin_screen.set_file_path(file_path)
    #
    #     # Connect the file uploader signal to update file paths in SelectDump
    #     self.file_uploader.file_path_updated.connect(self.select_dump.update_file_paths)

    # def closeEvent(self, event):
    #     self.session_manager.save_session()
    #     event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VolatilityApp()
    window.show()
    sys.exit(app.exec_())
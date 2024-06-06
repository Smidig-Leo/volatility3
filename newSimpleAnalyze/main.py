import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton
from screens.mainPage import MainPage
from screens.analyzeDataScreen import AnalyzeDataScreen
from newSimpleAnalyze.Components.fileUploader import FileUploader
from newSimpleAnalyze.Components.chooseOs import ChooseOs
from screens.pluginScreen import PluginScreen
from screens.settingsPage import SettingsPage
from newSimpleAnalyze.Components.selectDump import SelectDump
from newSimpleAnalyze.Components.runAnalysis import RunAnalysis
from newSimpleAnalyze.Components.selectPlugin import SelectPlugin
from PyQt5.uic import loadUi
from newSimpleAnalyze.data.sessionManager import SessionManager




class VolatilityApp(QMainWindow):
    activeCommandsUpdated = pyqtSignal(list)
    file_path_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        loadUi('screens/ui/NavigationBar.ui', self)
        self.setWindowTitle("Volatility3")

        # NavBar available buttons:
        # self.mainBtn
        # self.dataBtn
        # self.pluginsBtn
        # self.settingsBtn

        self.file_uploader = FileUploader()
        self.os = ChooseOs()
        self.select_dump = SelectDump()
        self.select_plugin = SelectPlugin()
        self.session_manager = SessionManager()
        self.run_analysis = RunAnalysis(self.select_dump, self.select_plugin)

        self.main_page = MainPage(self.file_uploader, self.os)
        self.plugins_page = PluginScreen(self.session_manager)
        self.data_page = AnalyzeDataScreen(self.file_uploader, self.select_dump, self.select_plugin,self.run_analysis)
        self.settings_page = SettingsPage()

        self.plugins_page.activeCommandsUpdated.connect(self.select_plugin.set_plugins)
        self.file_uploader.file_path_updated.connect(self.select_dump.update_file_paths)
        self.select_dump.file_selected.connect(self.run_analysis.handle_selected_files)
        self.select_dump.file_selected.connect(self.data_page.update_file_label)
        self.select_plugin.plugin_selected.connect(self.data_page.update_plugin_label)
        # Setup connections for the run analysis process
        self.select_plugin.plugin_selected.connect(self.run_analysis.handle_selected_plugin)
        self.run_analysis.analysis_result.connect(self.data_page.display_data)

        self.stackedWidget.addWidget(self.main_page)
        self.stackedWidget.addWidget(self.data_page)
        self.stackedWidget.addWidget(self.plugins_page)
        self.stackedWidget.addWidget(self.settings_page)

        self.plugins_page.activeCommandsUpdated.connect(self.on_active_commands_updated)

        self.main_page.analyzedButtonClicked.connect(self.switch_to_data_page)

        self.mainBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.main_page))
        self.dataBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.data_page))
        self.pluginsBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.plugins_page))
        self.settingsBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.settings_page))

    def switch_to_data_page(self):
        self.stackedWidget.setCurrentWidget(self.data_page)

    def on_active_commands_updated(self, active_commands):
        print(f"Received active commands update: {active_commands}")
        self.activeCommandsUpdated.emit(active_commands)


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
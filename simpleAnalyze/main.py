import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton
from screens.mainPage import MainPage
from screens.pluginScreen import PluginScreen
from screens.analyzeDataScreen import AnalyzeDataScreen
from data.sessionManager import SessionManager

class VolatilityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volatility App")
        self.setGeometry(100, 100, 800, 600)

        # Initialize session manager to store user state
        self.session_manager = SessionManager()
        self.session_manager.load_session()

        self.select_file_screen = MainPage(self)
        self.plugin_screen = PluginScreen()
        self.analyzed_data_screen = AnalyzeDataScreen()

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
        self.analyzed_data_screen.display_data(analyzed_result)

<<<<<<< HEAD
    def closeEvent(self, event):
        self.session_manager.save_session()
        event.accept()

=======
>>>>>>> 52a7967b59c8539ff413fc8d109a13491d4efbef
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VolatilityApp()
    window.show()
    sys.exit(app.exec_())
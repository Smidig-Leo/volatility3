from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import  loadUi

class SettingsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('screens/ui/Settings.ui', self)

        # available buttons:
        # self.radioButtonEnglish
        # self.radioButtonNorwegian
        # self.radioButtonDarkMode
        # self.radioButtonLightMode
        # self.radioButtonAllNotifications
        # self.radioButtonErrorMessages
        # self.radioButtonSucUplDwl
        # self.radioButtonAutoUpdate
        # self.pushButtonCheckUpdates
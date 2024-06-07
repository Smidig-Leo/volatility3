from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import  loadUi

class SettingsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('screens/ui/SettingsDark.ui', self)

        self.radioButtonDarkMode.toggled.connect(self.set_dark_mode)
        self.radioButtonLightMode.toggled.connect(self.set_light_mode)

    def set_dark_mode(self):
        if self.radioButtonDarkMode.isChecked():
            # Load the UI file for dark mode
            loadUi('screens/ui/SettingsDark.ui', self)
            self.setStyleSheet("")  # Clear any existing stylesheet

            # Reconnect radio buttons to methods
            self.radioButtonDarkMode.toggled.connect(self.set_dark_mode)
            self.radioButtonLightMode.toggled.connect(self.set_light_mode)

    def set_light_mode(self):
        if self.radioButtonLightMode.isChecked():
            # Load the UI file for light mode
            loadUi('screens/ui/SettingsLight.ui', self)
            self.setStyleSheet("")  # Clear any existing stylesheet

            # Reconnect radio buttons to methods
            self.radioButtonDarkMode.toggled.connect(self.set_dark_mode)
            self.radioButtonLightMode.toggled.connect(self.set_light_mode)
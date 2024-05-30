from PyQt5 import QtWidgets, uic
import sys


class SettingsPage(QtWidgets.QSettingsWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)

app = QtWidgets.QApplication(sys.argv)
window = SettingsPage()
window.show()
sys.exit(app.exec_())
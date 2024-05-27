from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
import sys, time
import subprocess

class Lavrans_PROGGRESSBAR_APP(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('first.ui', self)
        self.resize(930, 654)

        self.runButton.clicked.connect(self.run_command)
    
    def run_command(self):
        command = "python vol.py -f infected.vmem windows.pslist"
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.label.setText(stdout)
                self.label.adjustSize()
                self.frame.setMinimumSize(self.label.sizeHint())
            else:
                self.label.setText(f"Error: {stderr}")
        except Exception as e:
            print(f'An error occurred: {e}')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Lavrans_PROGGRESSBAR_APP()
    mainWindow.show()
    sys.exit(app.exec_())
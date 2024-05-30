from PyQt5.QtWidgets import QPushButton, QMenu, QAction, QVBoxLayout, QWidget

class ColumnsSort(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.columns_button = QPushButton("Columns")
        self.columns_button.setFixedSize(100, 30)

        menu = QMenu()
        options = ["pid", "process name", "process base", "size", "module name", "module path", "loadtime", "fileoutput"]
        for option in options:
            action = QAction(option, self, checkable=True)
            action.setChecked(True)
            menu.addAction(action)

        self.columns_button.setMenu(menu)
        layout.addWidget(self.columns_button)

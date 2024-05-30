from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView, QSizePolicy, QPushButton
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class DataTable(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.table_view = QTableView()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def update_table(self, data):
        if not data:
            return

        rows = data.strip().split('\n')
        headers = rows[2].split('\t')

        headers.append('Edit/Export')

        model = QStandardItemModel()
        model.setColumnCount(len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row_index, row in enumerate(rows[1:]):
            columns = row.split('\t')

            export_icon_path = 'Export.png'
            export_icon = QIcon(export_icon_path)

            import_button = QPushButton()
            import_button.setIcon(export_icon)
            import_button.setFixedSize(40, 40)

            import_button.setStyleSheet("background-color: red;")

            print("Adding button at row", row_index)

            for col_index, value in enumerate(columns):
                item = QStandardItem(value)
                model.setItem(row_index, col_index, item)

            # Add an empty item for the button column
            model.setItem(row_index, len(headers) - 1, QStandardItem())
            index = model.index(row_index, len(headers) - 1)
            self.table_view.setIndexWidget(index, import_button)

            widget = self.table_view.indexWidget(index)
            print(f"Widget at index ({row_index}, {len(headers) - 1}):", widget)

        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.resizeColumnsToContents()

        self.table_view.setColumnWidth(len(headers) - 1, 100)

        second_row_height = 50
        self.table_view.verticalHeader().resizeSection(1, second_row_height)
        self.table_view.verticalHeader().setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        for row in range(3):
            self.table_view.verticalHeader().hideSection(row)

        self.table_view.setAlternatingRowColors(True)

    def get_data(self):
        model = self.table_view.model()
        if not model:
            return []

        data = []
        for row in range(3, model.rowCount()):
            row_data = {}
            for col in range(model.columnCount()):
                index = model.index(row, col)
                header = model.headerData(col, Qt.Horizontal)
                value = model.data(index)
                row_data[header] = value
            data.append(row_data)

        return data

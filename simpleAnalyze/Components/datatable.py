from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView, QSizePolicy

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

        model = QStandardItemModel()
        model.setColumnCount(len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row_index, row in enumerate(rows[1:]):
            columns = row.split('\t')
            for col_index, value in enumerate(columns):
                item = QStandardItem(value)
                model.setItem(row_index, col_index, item)

        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.resizeColumnsToContents()

        second_row_height = 50
        self.table_view.verticalHeader().resizeSection(1, second_row_height)
        self.table_view.verticalHeader().setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        for row in range(3):
            self.table_view.verticalHeader().hideSection(row)

        self.table_view.setAlternatingRowColors(True)

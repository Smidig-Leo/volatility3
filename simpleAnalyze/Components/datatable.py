from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView, QSizePolicy, QPushButton
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex


class NumericSortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        left_data = self.sourceModel().data(left)
        right_data = self.sourceModel().data(right)

        if left_data is None:
            left_data = ""
        if right_data is None:
            right_data = ""

        try:
            left_data = float(left_data)
            right_data = float(right_data)
        except ValueError:
            left_data = str(left_data)
            right_data = str(right_data)

        return left_data < right_data


class DataTable(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.table_view = QTableView()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        self.proxy_model = NumericSortFilterProxyModel()
        self.table_view.setSortingEnabled(True)
        self.table_view.setModel(self.proxy_model)

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

            for col_index, value in enumerate(columns):
                item = QStandardItem(value)
                model.setItem(row_index, col_index, item)

            model.setItem(row_index, len(headers) - 1, QStandardItem())

        self.proxy_model.setSourceModel(model)

        for row_index in range(len(rows) - 1):
            export_button = QPushButton()

            export_icon = QIcon('export.png')
            export_button.setIcon(export_icon)

            export_button.setFixedSize(20, 20)

            index = model.index(row_index, len(headers) - 1)
            self.table_view.setIndexWidget(self.proxy_model.mapFromSource(index), export_button)

            widget = self.table_view.indexWidget(self.proxy_model.mapFromSource(index))
            print(f"Widget at index ({row_index}, {len(headers) - 1}):", widget)
            print(f"Column name: {headers[len(headers) - 1]}")

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
        model = self.proxy_model.sourceModel()
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
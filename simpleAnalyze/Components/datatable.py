from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableView, QHeaderView, QSizePolicy, QPushButton, QLabel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import xml.etree.ElementTree as ET

from simpleAnalyze.utils.exportmanager import ExportManager

class NumericSortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        left_data = self.sourceModel().data(left)
        right_data = self.sourceModel().data(right)

        if left_data is None or right_data is None:
            return False

        try:
            left_data = float(left_data)
            right_data = float(right_data)
        except ValueError:
            left_data = str(left_data)
            right_data = str(right_data)

        return left_data < right_data

class DataTable(QWidget):
    headers_updated = pyqtSignal(list)

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
            cell_widget = QWidget()
            cell_layout = QHBoxLayout()
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setSpacing(5)

            export_button = QPushButton("Export")
            export_button.setFixedSize(60, 21)
            export_button.clicked.connect(
                lambda _, row=row_index: self.export_row(row))
            cell_layout.addWidget(export_button)

            flag_button = QPushButton("Flag")
            flag_button.setFixedSize(60, 21)
            flag_button.clicked.connect(
                lambda _, button=flag_button: self.toggle_flag(button))
            flag_button.setProperty('flagged', False)
            cell_layout.addWidget(flag_button)

            cell_widget.setLayout(cell_layout)

            index = model.index(row_index, len(headers) - 1)
            self.table_view.setIndexWidget(self.proxy_model.mapFromSource(index), cell_widget)

        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(len(headers) - 1, 140)

        second_row_height = 50
        self.table_view.verticalHeader().resizeSection(1, second_row_height)
        self.table_view.verticalHeader().setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        for row in range(3):
            self.table_view.verticalHeader().hideSection(row)

        self.table_view.setAlternatingRowColors(True)

        self.headers_updated.emit(headers)

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

    def set_column_visibility(self, column_name, is_visible):
        model = self.proxy_model.sourceModel()
        if not model:
            return

        for col in range(model.columnCount()):
            header = model.headerData(col, Qt.Horizontal)
            if header == column_name:
                self.table_view.setColumnHidden(col, not is_visible)
                break

    def export_row(self, row):
        model = self.proxy_model.sourceModel()
        if not model:
            return

        data = []
        for col in range(model.columnCount()):
            index = model.index(row, col)
            header = model.headerData(col, Qt.Horizontal)
            value = model.data(index)
            data.append({header: value})

        ExportManager.export_data_as_xml(data, self)

    def toggle_flag(self, button):
        flagged = button.property('flagged')
        if flagged:
            button.setStyleSheet("")
        else:
            button.setStyleSheet("background-color: #ff6242; color: white; text-align: center;")
        button.setProperty('flagged', not flagged)

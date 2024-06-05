from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableView, QHeaderView, QSizePolicy, QPushButton, QLabel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush
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

        self.flagged_rows = set()

    def update_table(self, data):
        if not data:
            return

        # Parse data and color code
        all_rows_with_color = []
        for entry in data:
            color, rows_str = entry
            rows = [row.split('\t') for row in rows_str.strip().split('\n')[3:]]
            all_rows_with_color.extend([(row, color) for row in rows])

        # Set up model
        headers = data[0][1].strip().split('\n')[2].split('\t')
        headers.insert(0, 'File')  # Add 'File' column as the first column
        headers.append('Edit/Export')
        model = QStandardItemModel()
        model.setColumnCount(len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row_index, (columns, color) in enumerate(all_rows_with_color):
            for col_index, value in enumerate(columns):
                item = QStandardItem(value)
                model.setItem(row_index, col_index + 1, item)  # Adjust column index

            # Add color to the color column (which is now at index 0)
            color_item = QStandardItem()
            color_item.setBackground(QColor(color))
            model.setItem(row_index, 0, color_item)  # Set color column at index 0

            # Add button for each row
            cell_widget = QWidget()
            cell_layout = QHBoxLayout()
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setSpacing(5)

            export_button = QPushButton("Export")
            export_button.setFixedSize(60, 21)
            export_button.clicked.connect(lambda _, row=row_index: self.export_row(row))
            cell_layout.addWidget(export_button)

            flag_button = QPushButton("Flag")
            flag_button.setFixedSize(60, 21)
            flag_button.clicked.connect(lambda _, button=flag_button, row=row_index: self.toggle_flag(button, row))
            flag_button.setProperty('flagged', False)
            cell_layout.addWidget(flag_button)

            # Add color indicator based on provided color code
            color_indicator = QLabel("")
            color_indicator.setFixedSize(20, 20)
            color_indicator.setStyleSheet("background-color: {}".format(color))
            cell_layout.addWidget(color_indicator)

            cell_widget.setLayout(cell_layout)

            index = model.index(row_index, len(headers) - 1)  # Adjusted index for button column
            self.table_view.setIndexWidget(index, cell_widget)

        self.proxy_model.setSourceModel(model)

        # Set up table view properties
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(0, 40)  # Adjusted column index for color column

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

        ExportManager.export_data(data, self)

    def toggle_flag(self, button, row):
        flagged = button.property('flagged')
        model = self.proxy_model.sourceModel()

        if not flagged:
            for col in range(model.columnCount()):
                index = model.index(row, col)
                item = model.itemFromIndex(index)
                item.setBackground(QColor("#FF6242"))
            self.flagged_rows.add(row)
            button.setStyleSheet("background-color: #ff6242; color: white; text-align: center;")
        else:
            for col in range(model.columnCount()):
                index = model.index(row, col)
                item = model.itemFromIndex(index)
                item.setBackground(QBrush())
            self.flagged_rows.remove(row)
            button.setStyleSheet("")

        button.setProperty('flagged', not flagged)

def updatetable(self, data):
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
            lambda , row=rowindex: self.export_row(row))
        cell_layout.addWidget(export_button)

        flag_button = QPushButton("Flag")
        flag_button.setFixedSize(60, 21)
        flag_button.clicked.connect(
            lambda , button=flag_button, row=row_index: self.toggle_flag(button, row))
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


def update_table(self, data):
    if not data:
        return

    model = QStandardItemModel()

    if isinstance(data, str):
        rows = data.strip().split('\n')
        headers = rows[2].split('\t')
        headers.insert(0, 'File')  # Add 'File' column as the first column
        headers.append('Edit/Export')

        model.setColumnCount(len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row_index, row in enumerate(rows[1:]):
            columns = row.split('\t')
            for col_index, value in enumerate(columns):
                item = QStandardItem(value)
                model.setItem(row_index, col_index + 1, item)  # Adjust column index for 'File' insertion
            model.setItem(row_index, 0, QStandardItem())  # Insert 'File' item

            model.setItem(row_index, len(headers) - 1, QStandardItem())

    elif isinstance(data, list):
        all_rows_with_color = []
        for entry in data:
            color, rows_str = entry
            rows = [row.split('\t') for row in rows_str.strip().split('\n')[3:]]
            all_rows_with_color.extend([(row, color) for row in rows])

        headers = data[0][1].strip().split('\n')[2].split('\t')
        headers.insert(0, 'File')  # Add 'File' column as the first column
        headers.append('Edit/Export')

        model.setColumnCount(len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row_index, (columns, color) in enumerate(all_rows_with_color):
            color_item = QStandardItem()
            color_item.setBackground(QColor(color))
            model.setItem(row_index, 0, color_item)

            for col_index, value in enumerate(columns):
                item = QStandardItem(value)
                model.setItem(row_index, col_index + 1, item)  # Adjust column index for 'File' insertion

            model.setItem(row_index, len(headers) - 1, QStandardItem())

    self.proxy_model.setSourceModel(model)

    for row_index in range(model.rowCount()):
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

        if isinstance(data, list):
            color = all_rows_with_color[row_index][1]
            color_indicator = QLabel("")
            color_indicator.setFixedSize(20, 20)
            color_indicator.setStyleSheet(f"background-color: {color}")
            cell_layout.addWidget(color_indicator)

        cell_widget.setLayout(cell_layout)

        index = model.index(row_index, len(headers) - 1)
        self.table_view.setIndexWidget(self.proxy_model.mapFromSource(index), cell_widget)

    self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.table_view.resizeColumnsToContents()
    self.table_view.setColumnWidth(0, 40)
    self.table_view.setColumnWidth(len(headers) - 1, 140)

    second_row_height = 50
    self.table_view.verticalHeader().resizeSection(1, second_row_height)
    self.table_view.verticalHeader().setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    for row in range(3):
        self.table_view.verticalHeader().hideSection(row)

    self.table_view.setAlternatingRowColors(True)

    self.headers_updated.emit(headers)
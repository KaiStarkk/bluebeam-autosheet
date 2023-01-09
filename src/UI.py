from PyQt6 import QtCore, QtGui, QtWidgets
import PDF
import settings


class Table(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        config = settings.readConfig()
        super(Table, self).__init__(len(config["drawings"]), 5, parent)
        # ^ TODO - softload column count
        self._style_table()
        self._populate_table(config)
        # TODO - softload following items
        headertitle = ("Number", "Title", "Scale", "Discipline", "Type")
        self.setHorizontalHeaderLabels(headertitle)
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 250)
        self.setColumnWidth(2, 75)
        self.setColumnWidth(3, 100)
        self.setColumnWidth(4, 100)
        self.cellChanged.connect(self._cellclicked)

    def _cellclicked(self, r, c):
        it = self.item(r, c)
        it.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def _addrow(self):
        rowcount = self.rowCount()
        self.insertRow(rowcount)
        combox_add = QtWidgets.QComboBox(self)
        combox_add.addItems(["legend", "layout", "details", "SLD"])
        self.setCellWidget(rowcount, 4, combox_add)
        # ^ TODO - softload drawing types + qty of types

    def _removerow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)

    def _style_table(self):
        self.setFont(QtGui.QFont("Helvetica", 10, italic=False))
        self.verticalHeader().hide()
        self.horizontalHeader().setHighlightSections(False)
        self.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection)

    def _populate_table(self, config):
        # TODO - softload columns and describe their types in the data to simplify populating
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                current = list(config["drawings"].keys())[row]
                if (col == 4):
                    combox_lay = QtWidgets.QComboBox(self)
                    combox_lay.addItems(["legend", "layout", "details", "SLD"])
                    combox_lay.setCurrentText(
                        config["drawings"][current]["type"])
                    self.setCellWidget(row, col, combox_lay)
                else:
                    item = QtWidgets.QTableWidgetItem()
                    if (col == 0):
                        item.setText(current)
                    if (col == 1):
                        item.setText(config["drawings"][current]["title"])
                    if (col == 2):
                        item.setText(config["drawings"][current]["scale"])
                    if (col == 3):
                        item.setText(config["drawings"][current]["discipline"])
                    self.setItem(row, col, item)


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        config = settings.readConfig()
        table = Table()
        form_layout = self._create_form(config)
        button_layout = self._create_buttons(table, form_layout)
        hbox_layout = self._create_hbox(table)
        self._create_grid(form_layout, button_layout, hbox_layout)

    # TODO - review signatures for bad dependencies
    def _create_form(self, config):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(QtWidgets.QLabel("Project name:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["project name"]}'))
        form_layout.addRow(QtWidgets.QLabel("Project number:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["project number"]}'))
        form_layout.addRow(QtWidgets.QLabel("Client:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["client"]}'))
        form_layout.addRow(QtWidgets.QLabel("Issue date:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["issue date"]}'))
        form_layout.addRow(QtWidgets.QLabel("Issue description:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["issue description"]}'))
        form_layout.addRow(QtWidgets.QLabel("Construction status:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["construction status"]}'))
        form_layout.addRow(QtWidgets.QLabel("Stamp:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["stamp"]}'))
        form_layout.addRow(QtWidgets.QLabel("Approved by:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["approved by"]}'))
        form_layout.addRow(QtWidgets.QLabel("Drawn by:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["drawn by"]}'))
        form_layout.addRow(QtWidgets.QLabel("Rev:"),
                           QtWidgets.QLineEdit(f'{config["meta"]["rev"]}'))
        return form_layout

    def _create_buttons(self, table, form_layout):
        button_layout = QtWidgets.QVBoxLayout()
        add_button = QtWidgets.QPushButton("Add")
        add_button.clicked.connect(table._addrow)
        delete_button = QtWidgets.QPushButton("Delete")
        delete_button.clicked.connect(table._removerow)
        save_button = QtWidgets.QPushButton("Save Config")
        save_button.clicked.connect(
            lambda: settings.saveConfig(settings.readConfig(), form_layout, table))
        run_button = QtWidgets.QPushButton("Run Setup")
        run_button.clicked.connect(PDF.process_templates)
        button_layout.addWidget(
            add_button, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        button_layout.addWidget(
            delete_button, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        button_layout.addWidget(
            save_button, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        button_layout.addWidget(
            run_button, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        return button_layout

    def _create_hbox(self, table):
        hbox_layout = QtWidgets.QHBoxLayout()
        hbox_layout.setContentsMargins(10, 10, 10, 10)
        hbox_layout.addWidget(table)
        return hbox_layout

    def _create_grid(self, form_layout, button_layout, hbox_layout):
        grid = QtWidgets.QGridLayout(self)
        self.resize(800, 550)
        grid.addLayout(form_layout, 0, 0)
        grid.addLayout(button_layout, 1, 1)
        grid.addLayout(hbox_layout, 1, 0)


def style_app(app):
    app.setStyle("Fusion")
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ColorRole.WindowText,
                     QtGui.QColorConstants.LightGray)
    palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(25, 25, 25))
    palette.setColor(QtGui.QPalette.ColorRole.AlternateBase,
                     QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ColorRole.ToolTipBase,
                     QtGui.QColorConstants.Black)
    palette.setColor(QtGui.QPalette.ColorRole.ToolTipText,
                     QtGui.QColorConstants.LightGray)
    palette.setColor(QtGui.QPalette.ColorRole.Text,
                     QtGui.QColorConstants.LightGray)
    palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ColorRole.ButtonText,
                     QtGui.QColorConstants.LightGray)
    palette.setColor(QtGui.QPalette.ColorRole.BrightText,
                     QtGui.QColorConstants.Red)
    palette.setColor(QtGui.QPalette.ColorRole.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.ColorRole.Highlight,
                     QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.ColorRole.HighlightedText,
                     QtGui.QColorConstants.Black)
    app.setPalette(palette)


def error_box(code):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText("Something went wrong: {0}".format(code))
    msg.exec()

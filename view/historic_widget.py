from PyQt6.QtWidgets import QWidget
from PyQt6 import uic


import pathlib
ui_dir = pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), 'ui')
historic_widget_file = pathlib.Path.joinpath(ui_dir, 'historic_widget.ui')
app_dir = pathlib.Path(__file__).parent.parent.resolve()


class HistoricWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(historic_widget_file, self)

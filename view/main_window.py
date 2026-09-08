from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction
from PyQt6 import uic
from dataclasses import dataclass
from database.options import OptionValue
import json
from database.projects import Project, Element, Record, db_observer, init_database


import pathlib
ui_dir = pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), 'ui')
main_windows_file = pathlib.Path.joinpath(ui_dir, 'main_window.ui')
app_dir = pathlib.Path(__file__).parent.parent.resolve()


@dataclass
class CurrentState:
    db_opened: bool = False
    current_stream: Project|None = None
    current_element: Element|None = None
    current_record: Record|None = None
    current_open_db: str|None = None


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Plan'n'Run DB")
        db_observer.add_observer(self)
        self.current_state = CurrentState()

        # Load the UI from the .ui file
        uic.loadUi(main_windows_file, self)

        # Load the open database history from the options database
        history_json = OptionValue.get(OptionValue.key == 'open_db_history').value
        self.current_state.history_open_db = json.loads(history_json)
        for db_name in self.current_state.history_open_db:
            new_menu  = QAction(db_name, self)
            new_menu.triggered.connect(lambda _, name=db_name: self._open_database(name))
            self.database_history_menu.addAction(new_menu)

    def _open_database(self, file_path):
        init_database(file_path)
        self.current_state.db_opened = True
        self.current_state.current_open_db = file_path
        self.current_db_label.setText(f"Database: {self.current_state.current_open_db}")
        self.load_project_table()
        print("Database opened from history at:", file_path)

    def load_project_table(self):
        # Implement the logic to load the project table here
        pass

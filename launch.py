from PyQt6.QtWidgets import QApplication
from view.main_window import MainWindow
from database.options import init_option_database
import sys


if __name__ == '__main__':
    init_option_database()
    app = QApplication(sys.argv)
    app.quitOnLastWindowClosed = True
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())

import sys
from PyQt6.QtWidgets import QApplication
from view.app_view import MainWindow
from lst_parser_bits import Listing

lst = Listing()

Qapp = QApplication(sys.argv)
window = MainWindow()
window.init_window()
Qapp.exec()
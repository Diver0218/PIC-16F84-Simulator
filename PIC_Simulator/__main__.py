import sys
from PyQt6.QtWidgets import QApplication
from view.app_view import MainWindow

Qapp = QApplication(sys.argv)
window = MainWindow()
window.init_window()
Qapp.exec()
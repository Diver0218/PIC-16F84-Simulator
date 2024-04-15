import sys
from control.processor import Processor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread
from view.app_view import MainWindow
from lst_parser_bits import Listing

lst = Listing()

Qapp = QApplication(sys.argv)
window = MainWindow()
window.init_window()
p = Processor(lst.get_instructions())
p_thread = QThread()
p.moveToThread(p_thread)
Qapp.exec()
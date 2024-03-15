from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from ..__main__ import update_mem_gui
#from model.memory import Register


class MemTable(QTableWidget):

    data : list

    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self, data):
        horHeaders = ['Adress', 'Bit 0', 'Bit 1', 'Bit 2', 'Bit 3', 'Bit 4', 'Bit 5', 'Bit 6', 'Bit 6', 'Full Value']
        rows = self.rowCount()
        columns = self.columnCount()
        adress = 0
        for i in range(rows):
            for j in range(columns):
                if j == 0:
                    item = adress
                    newitem = QTableWidgetItem(str(item))
                    self.setItem(i , j, newitem)
                    adress += 1
                elif j == 9:
                    item = data[i].value
                    newitem = QTableWidgetItem(str(item))
                    self.setItem(i , j, newitem)
                else:
                    item = data[i].test_bit(j - 1)
                    newitem = QTableWidgetItem(str(item))
                    self.setItem(i , j, newitem)
        self.setHorizontalHeaderLabels(horHeaders)


class BaseWindow():

    app = QApplication([])
    window = QWidget()
    lay_h = QHBoxLayout()
    lay_v = QVBoxLayout()
    lbl_code = QLabel("Test Text")
    btn_run = QPushButton('Run')
    tbl_memory = MemTable("test", 80, 10)
    tableData : list

    def __init__(self, tableData):
        self.create_window()
        self.tableData = tableData

    def create_window(self):
        self.lay_h.addWidget(self.lbl_code)
        self.lay_h.addWidget(self.tbl_memory)

        self.lay_v.addLayout(self.lay_h)
        self.lay_v.addWidget(self.btn_run)

        self.btn_run.clicked.connect(self.on_click_run)

        self.window.setLayout(self.lay_v)
        self.window.resize(800, 600)

    def init_window(self):
        self.window.show()
        self.setMemData(self.tableData)
        self.tbl_memory.show()
        self.app.exec()

    def setMemData(self, data):
        self.tbl_memory.setData(data)

    def on_click_run(self):
        self.setMemData(self.tableData)
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit
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
    lay_main = QHBoxLayout()
    lay_reg = QVBoxLayout()
    lay_code = QVBoxLayout()
    lay_runctrl = QVBoxLayout()
    lay_brk = QHBoxLayout()
    lay_freq = QHBoxLayout()
    lbl_code = QLabel("Test Textldkgujkliguroiuaerhglreiugherpiughergiuerjhgeruigherwo\ngiherögoierhgoerihgeraoighWEÄPGOEWUÜGPEOGJEÖIGewöogiwegöWELIHGÖweoi")
    btn_step = QPushButton('Step')
    btn_run = QPushButton('Run')
    btn_stop = QPushButton('Stop')
    btn_reset = QPushButton('Reset')
    txtbox_brk = QLineEdit("-")
    txtbox_freq = QLineEdit("4.0")
    btn_setbrk = QPushButton('Set')
    btn_setfreq = QPushButton('Set')
    lbl_timer = QLabel("0us")
    tbl_porta = MemTable("test", 80, 10)
    tbl_portb = MemTable("test", 80, 10)
    tbl_mem = MemTable("test", 80, 10)
    lbl_sfr = QLabel("SFR")
    tableData : list

    def __init__(self, tableData):
        self.create_window()
        self.tableData = tableData

    def create_window(self):
        self.lay_reg.addWidget(self.tbl_porta)
        self.lay_reg.addWidget(self.tbl_portb)
        self.lay_reg.addWidget(self.tbl_mem)
        
        self.lay_code.addWidget(self.lbl_code)
        
        self.lay_runctrl.addWidget(self.btn_step)
        self.lay_runctrl.addWidget(self.btn_run)
        self.lay_runctrl.addWidget(self.btn_stop)
        self.lay_runctrl.addWidget(self.btn_reset)
        
        self.lay_brk.addWidget(self.txtbox_brk)
        self.lay_brk.addWidget(self.btn_setbrk)
        
        self.lay_freq.addWidget(self.txtbox_freq)
        self.lay_freq.addWidget(self.btn_setfreq)
        
        self.lay_runctrl.addLayout(self.lay_brk)
        self.lay_runctrl.addLayout(self.lay_freq)
        
        self.lay_runctrl.addWidget(self.lbl_timer)
        
        self.lay_main.addLayout(self.lay_reg)
        self.lay_main.addLayout(self.lay_code)
        self.lay_main.addLayout(self.lay_runctrl)

        self.window.setLayout(self.lay_main)
        self.window.resize(800, 600)

    def init_window(self):
        self.window.show()
        self.setMemData(self.tableData)
        self.tbl_mem.show()
        self.app.exec()

    def setMemData(self, data):
        self.tbl_mem.setData(data)

    def on_click_run(self):
        self.setMemData(self.tableData)
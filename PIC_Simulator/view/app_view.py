from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QMainWindow
from PyQt6.QtWidgets import QLineEdit
import sys

from control.processor import Processor
from lst_parser_bits import Listing



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
    
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

    def create_window(self): 
##########################
#ACHTUNG nur zum testen
        self.lst = Listing()
        self.p = Processor(self.lst.get_instructions())
##########################
        self.lay_main = QHBoxLayout()
        self.lay_reg = QVBoxLayout()
        self.lay_code = QVBoxLayout()
        self.lay_runctrl = QVBoxLayout()
        self.lay_brk = QHBoxLayout()
        self.lay_freq = QHBoxLayout()
        self.lbl_code = QLabel("lskdugaldkgjsdlgkjbasdjgkbsdjgdfgdGSDGsdds\nwefwefewfwefwefwefWEFWefWEGWegewG\n hfgduzsgkeriugziebsztieruztvgerzuvteuzteriuvziguzrgiuzrgkazgrzaergkzeragkreuz")
        self.btn_step = QPushButton('Step')
        self.btn_run = QPushButton('Run')
        self.btn_stop = QPushButton('Stop')
        self.btn_reset = QPushButton('Reset')
        self.txtbox_brk = QLineEdit("-")
        self.txtbox_freq = QLineEdit("4.0")
        self.btn_setbrk = QPushButton('Set')
        self.btn_setfreq = QPushButton('Set')
        self.lbl_timer = QLabel("0us")
        self.tbl_porta = MemTable("test", 80, 10)
        self.tbl_portb = MemTable("test", 80, 10)
        self.tbl_mem = MemTable("test", 80, 10)
        self.lbl_sfr = QLabel("SFR")
        self.tableData : list
        
        self.menubar = QMenuBar(self)
        file_menu = QMenu("Datei", self)
        open_action = file_menu.addAction("Öffnen")
        self.menubar.addMenu(file_menu)

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

        self.setLayout(self.lay_main)
        self.resize(800, 600)

    def init_window(self):
        self.create_window()
        self.show()
        self.setMemData()
        self.tbl_mem.show()

    def setMemData(self):
        self.tbl_mem.setData(self.p.mem)

    
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QMainWindow, QSizePolicy
from PyQt6.QtWidgets import QLineEdit
import sys

from control.processor import Processor
from lst_parser_bits import Listing



class MemTable(QTableWidget):

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self, mem):
        rows = self.rowCount()
        columns = self.columnCount()
        verticaHeaders = []
        for i in range(rows):
            for j in range(columns):
                if j == 8:
                    item = mem[i].value
                    newitem = QTableWidgetItem(str(item))
                    self.setItem(i , j, newitem)
                else:
                    item = mem[i].test_bit(j)
                    newitem = QTableWidgetItem(str(item))
                    self.setItem(i , j, newitem)
            verticaHeaders.append(str(hex(i))[2:])
        self.setVerticalHeaderLabels(verticaHeaders)

    
    def setPortData(self, mem, adr):
        rows = self.rowCount()
        columns = self.columnCount()
        for i in range(columns):
            self.setItem(2, i, QTableWidgetItem(str(mem[adr].test_bit(7 - i))))
        for i in range(columns):
            item = mem[adr].test_bit(7 - i) #adr muss noch um +0x80 verschoben werden
            self.setItem(0, i, QTableWidgetItem(str(item)))
            if item:
                self.setItem(1, i, QTableWidgetItem('i'))
            else:
                self.setItem(1, i, QTableWidgetItem('o'))
        
            
    
    
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('PIC-16F84-Simulator')

    def create_window(self): 
##########################
#ACHTUNG nur zum testen
        self.lst = Listing()
        self.p = Processor(self.lst.get_instructions())
##########################
        widg_main = QWidget()
        lay_main = QHBoxLayout()
        lay_reg = QVBoxLayout()
        lay_code = QVBoxLayout()
        lay_runctrl = QVBoxLayout()
        lay_brk = QHBoxLayout()
        lay_freq = QHBoxLayout()
        lbl_code = QLabel("lskdugaldkgjsdlgkjbasdjgkbsdjgdfgdGSDGsdds\nwefwefewfwefwefwefWEFWefWEGWegewG\n hfgduzsgkeriugziebsztieruztvgerzuvteuzteriuvziguzrgiuzrgkazgrzaergkzeragkreuz")
        btn_step = QPushButton('Step')
        btn_run = QPushButton('Run')
        btn_stop = QPushButton('Stop')
        btn_reset = QPushButton('Reset')
        txtbox_brk = QLineEdit("-")
        txtbox_freq = QLineEdit("4.0")
        btn_setbrk = QPushButton('Set')
        btn_setfreq = QPushButton('Set')
        lbl_timer = QLabel("0us")
        self.tbl_porta = MemTable(3, 8)
        self.tbl_portb = MemTable(3, 8)
        self.tbl_mem = MemTable(80, 9)
        lbl_sfr = QLabel("SFR")
        tableData : list
        
        menubar = QMenuBar(self)
        file_menu = QMenu("Datei", self)
        open_action = file_menu.addAction("Öffnen")
        menubar.addMenu(file_menu)

        widg_main.setWindowTitle('PIC-16F84-Simulator')
        
        self.tbl_porta.setHorizontalHeaderLabels(['RA 7','RA 6','RA 5','RA 4','RA 3','RA 2','RA 1','RA 0'])
        self.tbl_porta.setVerticalHeaderLabels(['TRIS','i/o','RA'])
        self.tbl_portb.setHorizontalHeaderLabels(['RB 7','RB 6','RB 5','RB 4','RB 3','RB 2','RB 1','RB 0'])
        self.tbl_portb.setVerticalHeaderLabels(['TRIS','i/o','RB'])
        self.tbl_mem.setHorizontalHeaderLabels(['Adress', 'Bit 0', 'Bit 1', 'Bit 2', 'Bit 3', 'Bit 4', 'Bit 5', 'Bit 6', 'Bit 6', 'Full Value'])
        
        lay_reg.addWidget(self.tbl_porta)
        lay_reg.addWidget(self.tbl_portb)
        lay_reg.addWidget(self.tbl_mem)
        
        lay_code.addWidget(lbl_code)
        
        lay_runctrl.addWidget(btn_step)
        lay_runctrl.addWidget(btn_run)
        lay_runctrl.addWidget(btn_stop)
        lay_runctrl.addWidget(btn_reset)
        
        lay_brk.addWidget(txtbox_brk)
        lay_brk.addWidget(btn_setbrk)
        
        lay_freq.addWidget(txtbox_freq)
        lay_freq.addWidget(btn_setfreq)
        
        lay_runctrl.addLayout(lay_brk)
        lay_runctrl.addLayout(lay_freq)
        
        lay_runctrl.addWidget(lbl_timer)
        
        lay_main.addLayout(lay_reg)
        lay_main.addLayout(lay_code)
        lay_main.addLayout(lay_runctrl)

        widg_main.setLayout(lay_main)
        widg_main.setGeometry(0, menubar.height(), 0, 0)
        
        self.setMenuBar(menubar)
        self.setCentralWidget(widg_main)
        menubar.raise_()
        self.resize(800, 600)
        

    def init_window(self):
        self.create_window()
        self.show()
        self.setMemData()
        self.tbl_mem.show()

    def setMemData(self):
        self.tbl_mem.setData(self.p.mem)
        self.tbl_porta.setPortData(self.p.mem, 5)
        self.tbl_portb.setPortData(self.p.mem, 6)
        

    

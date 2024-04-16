from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QMainWindow, QLayout
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QRect
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

        #main
        widg_main = QWidget()
        lay_main = QHBoxLayout()
        
        #regs
        widg_reg = QWidget(parent=widg_main)
        widg_reg.setGeometry(QRect(0, 0, 1631, 2000))
        lay_reg = QVBoxLayout(widg_reg)
        self.tbl_porta = MemTable(3, 8)
        self.tbl_portb = MemTable(3, 8)
        self.tbl_mem = MemTable(80, 9)
        lbl_sfr = QLabel("SFR")
        
        self.tbl_porta.setHorizontalHeaderLabels(['RA 7','RA 6','RA 5','RA 4','RA 3','RA 2','RA 1','RA 0'])
        self.tbl_porta.setVerticalHeaderLabels(['TRIS','i/o','RA'])
        self.tbl_porta.resizeColumnsToContents()
        self.tbl_porta.resizeRowsToContents()
        self.tbl_porta.setFixedSize(348, 98)
        self.tbl_portb.setHorizontalHeaderLabels(['RB 7','RB 6','RB 5','RB 4','RB 3','RB 2','RB 1','RB 0'])
        self.tbl_portb.setVerticalHeaderLabels(['TRIS','i/o','RB'])
        self.tbl_portb.resizeColumnsToContents()
        self.tbl_portb.resizeRowsToContents()
        self.tbl_portb.setFixedSize(348, 98)
        self.tbl_mem.setHorizontalHeaderLabels(['Bit 0', 'Bit 1', 'Bit 2', 'Bit 3', 'Bit 4', 'Bit 5', 'Bit 6', 'Bit 6', 'Value'])
        self.tbl_mem.resizeColumnsToContents()
        self.tbl_mem.resizeRowsToContents()
        self.tbl_mem.setFixedWidth(392)
        
        lay_reg.addWidget(self.tbl_porta)
        lay_reg.addWidget(self.tbl_portb)
        lay_reg.addWidget(self.tbl_mem)
        lay_reg.setStretch(0, 28)
        lay_reg.setStretch(1, 28)
        lay_reg.setStretch(2, 64)
        
        
        #Code
        widg_code = QWidget(parent=widg_main)
        lay_code = QVBoxLayout(widg_code)
        lbl_code = QLabel("lskdugaldkgjsdlgkjbasdjgkbsdjgdfgdGSDGsdds\nwefwefewfwefwefwefWEFWefWEGWegewG\n hfgduzsgkeriugziebsztieruztvgerzuvteuzteriuvziguzrgiuzrgkazgrzaergkzeragkreuz")
        
        lay_code.addWidget(lbl_code)
        
        #Run Control
        widg_runctrl = QWidget(parent=widg_main)
        lay_runctrl = QVBoxLayout(widg_runctrl)
        
        widg_brk = QWidget(parent=widg_runctrl)
        lay_brk = QHBoxLayout(widg_brk)
        
        widg_freq = QWidget(parent=widg_runctrl)
        lay_freq = QHBoxLayout(widg_freq)
        
        btn_step = QPushButton('Step')
        btn_run = QPushButton('Run')
        btn_stop = QPushButton('Stop')
        btn_reset = QPushButton('Reset')
        txtbox_brk = QLineEdit("-")
        txtbox_freq = QLineEdit("4.0")
        btn_setbrk = QPushButton('Set')
        btn_setfreq = QPushButton('Set')
        lbl_timer = QLabel("0us")
        tableData : list
        
        lay_runctrl.addWidget(btn_step)
        lay_runctrl.addWidget(btn_run)
        lay_runctrl.addWidget(btn_stop)
        lay_runctrl.addWidget(btn_reset)
        
        lay_brk.addWidget(txtbox_brk)
        lay_brk.addWidget(btn_setbrk)
        
        lay_freq.addWidget(txtbox_freq)
        lay_freq.addWidget(btn_setfreq)
        
        lay_runctrl.addWidget(widg_brk)
        lay_runctrl.addWidget(widg_freq)
        
        lay_runctrl.addWidget(lbl_timer)
        
        
        #menubar
        menubar = QMenuBar(self)
        file_menu = QMenu("Datei", self)
        open_action = file_menu.addAction("Öffnen")
        menubar.addMenu(file_menu)

        self.setMenuBar(menubar)
        self.setCentralWidget(widg_main)
        menubar.raise_()
        self.resize(1200, 600)
        
        
        #Complete
        lay_main.addWidget(widg_reg)
        lay_main.addWidget(widg_code)
        lay_main.addWidget(widg_runctrl)
        lay_main.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        widg_main.setLayout(lay_main)
        widg_main.setWindowTitle('PIC-16F84-Simulator')
        

    def init_window(self):
        self.create_window()
        self.show()
        self.setMemData()
        self.tbl_mem.show()

    def setMemData(self):
        self.tbl_mem.setData(self.p.mem)
        self.tbl_porta.setPortData(self.p.mem, 5)
        self.tbl_portb.setPortData(self.p.mem, 6)
        

    

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QMainWindow, QLayout, QFileDialog
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QRect
import sys
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
from control.processor import Processor
from lst_parser_bits import Listing
from pathlib import Path
from model.memory import Memory
#debug
from PyQt6.QtWidgets import QDialog
#enddebug



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

    lst = Listing()
    
    sig_steprequest = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('PIC-16F84-Simulator')

    def create_window(self): 
##########################
#ACHTUNG nur zum testen
        #self.lst = Listing()
        #self.p = Processor(self.lst.get_instructions())
##########################

        #main
        self.widg_main = QWidget()
        self.lay_main = QHBoxLayout()
        
        #regs
        self.widg_reg = QWidget(parent=self.widg_main)
        self.widg_reg.setGeometry(QRect(0, 0, 1631, 2000))
        self.lay_reg = QVBoxLayout(self.widg_reg)
        self.tbl_porta = MemTable(3, 8)
        self.tbl_portb = MemTable(3, 8)
        self.tbl_mem = MemTable(80, 9)
        self.lbl_sfr = QLabel("SFR")
        
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
        
        self.lay_reg.addWidget(self.tbl_porta)
        self.lay_reg.addWidget(self.tbl_portb)
        self.lay_reg.addWidget(self.tbl_mem)
        
        
        #Code
        self.widg_code = QWidget(parent=self.widg_main)
        self.lay_code = QVBoxLayout(self.widg_code)
        self.lbl_code = QLabel("lskdugaldkgjsdlgkjbasdjgkbsdjgdfgdGSDGsdds\nwefwefewfwefwefwefWEFWefWEGWegewG\n hfgduzsgkeriugziebsztieruztvgerzuvteuzteriuvziguzrgiuzrgkazgrzaergkzeragkreuz")

        self.lay_code.addWidget(self.lbl_code)
        
        #Run Control
        self.widg_runctrl = QWidget(parent=self.widg_main)
        self.lay_runctrl = QVBoxLayout(self.widg_runctrl)
        
        self.widg_brk = QWidget(parent=self.widg_runctrl)
        self.lay_brk = QHBoxLayout(self.widg_brk)
        
        self.widg_freq = QWidget(parent=self.widg_runctrl)
        self.lay_freq = QHBoxLayout(self.widg_freq)
        
        self.btn_step = QPushButton('Step')
        self.btn_run = QPushButton('Run')
        self.btn_stop = QPushButton('Stop')
        self.btn_reset = QPushButton('Reset')
        self.txtbox_brk = QLineEdit("-")
        self.txtbox_freq = QLineEdit("4.0")
        self.btn_setbrk = QPushButton('Set')
        self.btn_setfreq = QPushButton('Set')
        self.lbl_timer = QLabel("0us")
        self.tableData : list
        
        self.btn_step.clicked.connect(self.btn_step_method)
        
        self.lay_runctrl.addWidget(self.btn_step)
        self.lay_runctrl.addWidget(self.btn_run)
        self.lay_runctrl.addWidget(self.btn_stop)
        self.lay_runctrl.addWidget(self.btn_reset)
        
        self.lay_brk.addWidget(self.txtbox_brk)
        self.lay_brk.addWidget(self.btn_setbrk)
        
        self.lay_freq.addWidget(self.txtbox_freq)
        self.lay_freq.addWidget(self.btn_setfreq)
        
        self.lay_runctrl.addWidget(self.widg_brk)
        self.lay_runctrl.addWidget(self.widg_freq)
        
        self.lay_runctrl.addWidget(self.lbl_timer)
        
        
        #menubar
        menubar = QMenuBar(self)
        file_menu = QMenu("Datei", self)
        self.open_action = file_menu.addAction("Öffnen")
        menubar.addMenu(file_menu)
        self.open_action.triggered.connect(self.open_file)

        self.setMenuBar(menubar)
        self.setCentralWidget(self.widg_main)
        menubar.raise_()
        self.resize(1200, 600)
        
        
        #Complete
        self.lay_main.addWidget(self.widg_reg)
        self.lay_main.addWidget(self.widg_code)
        self.lay_main.addWidget(self.widg_runctrl)
        self.lay_main.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        self.widg_main.setLayout(self.lay_main)
        self.widg_main.setWindowTitle('PIC-16F84-Simulator')
        

    def init_window(self):
        self.create_window()
        self.show()
        self.tbl_mem.show()

    @pyqtSlot(Memory)
    def setMemData(self, data):
        #debug:
        #print("Funktion aufgerufen: setMemData")
        #enddebug
        self.tbl_mem.setData(data)
        self.tbl_porta.setPortData(data, 5)
        self.tbl_portb.setPortData(data, 6)

    @pyqtSlot()
    def btn_step_method(self):
        #debug
        print("Funktion aufgerufen: btn_step_method")
        #enddebug
        self.sig_steprequest.emit(True)
    
    @pyqtSlot()
    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "Listing (*.LST);; All Files (*)")
        self.lst.create_instructions(filename[0])
        with open(filename[0], 'r') as file:
            try:
                self.p_thread.terminate()
            except Exception:
                pass
                
            self.lbl_code.setText(file.read())
            self.p = Processor(self.lst.get_instructions())
        self.p.sig_mem.connect(self.setMemData)
        self.sig_steprequest.connect(self.p.step)
        self.p_thread = QThread()
        self.p.moveToThread(self.p_thread)
        self.p_thread.start()
           
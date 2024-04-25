from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QMainWindow, QLayout, QFileDialog
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QRect
import sys
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from control.processor import Processor
from lst_parser_bits import Listing
from pathlib import Path
from model.memory import Memory
#debug
from PyQt6.QtWidgets import QDialog
from PyQt6 import QtGui
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
                    item = mem.get_bank_specific_register(i, 0).value
                    newitem = QTableWidgetItem(str(item))
                    self.setItem(i , j, newitem)
                else:
                    item = mem.get_bank_specific_register(i, 0).test_bit(j)
                    newitem = QTableWidgetItem(str(item))
                    self.setItem(i , j, newitem)
            verticaHeaders.append(str(hex(i))[2:])
        self.setVerticalHeaderLabels(verticaHeaders)

    
    def setPortData(self, mem, adr):
        rows = self.rowCount()
        columns = self.columnCount()
        for i in range(columns):
            tbl_button = TblPortButton()
            tbl_button.setText(str(mem.get_bank_specific_register(adr, 0).test_bit(7 - i)))
            self.setCellWidget(2, i, tbl_button)
        for i in range(columns):
            item = mem.get_bank_specific_register(adr, 1).test_bit(7 - i) #adr muss noch um +0x80 verschoben werden
            self.setItem(0, i, QTableWidgetItem(str(item))) # evtl hier auch ToggleButton einfügen
            if item:
                self.setItem(1, i, QTableWidgetItem('i'))
            else:
                self.setItem(1, i, QTableWidgetItem('o'))

    def resizePorts(self):
        for i in range(7):
            self.rowResized(i, 5, 5)
            self.columnResized(i, 5, 5)
        self.setFixedSize(292, 98)
        
            
class TblPortButton(QPushButton):
    def __init__(self, parent=None):
        super(TblPortButton, self).__init__(parent)
        self.clicked.connect(self.toggleButton)
        
    def toggleButton(self): #Muss noch mit Memory verbunden werden
        if self.text() == '1':
            self.setText('0')
        else:
            self.setText('1')
    
class MainWindow(QMainWindow):
    
    sig_steprequest = pyqtSignal(bool)
    sig_init = pyqtSignal(bool)
    code_lbls = []

    def __init__(self):
        super().__init__()
        self.lst = Listing("")

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
        self.lay_reg = QVBoxLayout(self.widg_reg)
        self.tbl_porta = MemTable(3, 8)
        self.tbl_portb = MemTable(3, 8)
        self.tbl_mem = MemTable(80, 9)
        self.lbl_sfr = QLabel("SFR")
        
        self.tbl_porta.setHorizontalHeaderLabels(['RA 7','RA 6','RA 5','RA 4','RA 3','RA 2','RA 1','RA 0'])
        self.tbl_porta.setVerticalHeaderLabels(['TRIS','i/o','RA'])
        self.tbl_porta.resizePorts()
        self.tbl_portb.setHorizontalHeaderLabels(['RB 7','RB 6','RB 5','RB 4','RB 3','RB 2','RB 1','RB 0'])
        self.tbl_portb.setVerticalHeaderLabels(['TRIS','i/o','RB'])
        self.tbl_portb.resizePorts()
        self.tbl_mem.setHorizontalHeaderLabels(['Bit 0', 'Bit 1', 'Bit 2', 'Bit 3', 'Bit 4', 'Bit 5', 'Bit 6', 'Bit 6', 'Value'])
        self.tbl_mem.resizeColumnsToContents()
        self.tbl_mem.resizeRowsToContents()
        self.tbl_mem.setFixedWidth(353)
        
        self.lay_reg.addWidget(self.tbl_porta)
        self.lay_reg.addWidget(self.tbl_portb)
        self.lay_reg.addWidget(self.tbl_mem)
        
        
        #Code
        self.widg_code = QWidget(parent=self.widg_main)
        self.lay_code = QVBoxLayout(self.widg_code)
        self.list_code = QListWidget()
        # self.lbl_code = QLabel("lskdugaldkgjsdlgkjbasdjgkbsdjgdfgdGSDGsdds\nwefwefewfwefwefwefWEFWefWEGWegewG\n hfgduzsgkeriugziebsztieruztvgerzuvteuzteriuvziguzrgiuzrgkazgrzaergkzeragkreuz")

        self.lay_code.addWidget(self.list_code)
        
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
        
        
        #Complete
        self.lay_main.addWidget(self.widg_reg)
        self.lay_main.addWidget(self.widg_code)
        self.lay_main.addWidget(self.widg_runctrl)
        self.lay_main.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        self.widg_main.setLayout(self.lay_main)
        self.widg_main.setWindowTitle('PIC-16F84-Simulator')
        self.resize(1200, 600)
        

    def init_window(self):
        self.create_window()
        self.show()
        self.tbl_mem.show()
        self.setMemData(Memory())

    @pyqtSlot(Memory)
    def setMemData(self, mem):
        #debug:
        #print("Funktion aufgerufen: setMemData")
        #enddebug
        self.tbl_mem.setData(mem)
        self.tbl_porta.setPortData(mem, 5)
        self.tbl_portb.setPortData(mem, 6)

    @pyqtSlot()
    def btn_step_method(self):
        self.sig_steprequest.emit(True)
    
    @pyqtSlot()
    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "Listing (*.LST);; All Files (*)")
        if not filename[0]:
            return
        self.lst = Listing(filename[0])
        with open(filename[0], 'r') as file:
            try:
                self.p_thread.terminate()
                print("Thread terminated")
            except Exception:
                print("No Thread to termina te")
            self.init_new_processor()
            self.show_Code(file)
            print(self.lst.get_instructions())
            
    def init_new_processor(self):
        self.p = Processor(self.lst.get_instructions())
        self.p.sig_mem.connect(self.setMemData)
        self.sig_steprequest.connect(self.p.step)
        self.p.sig_pc.connect(self.highlight_instruction)
        self.sig_init.connect(self.p.init_view)
        self.p_thread = QThread()
        self.p.moveToThread(self.p_thread)
        self.p_thread.start()

    def show_Code(self, file):
        if self.code_lbls:
            for line in self.code_lbls:
                self.list_code.clear()
        self.code_lbls = []
        for line in file:
            if line[0] != ' ':
                pc = int(line[0:4], 16)
            else:
                pc = -1
            item = QListWidgetItem(line)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            item.setFont(QtGui.QFont('Consolas', 10))
            self.code_lbls.append({
                'pc' : pc,
                'label' : item
            })
        for line in self.code_lbls:
            self.list_code.addItem(line['label'])
        i = 0
        while self.code_lbls[i]['pc'] != 0:
            i += 1
        self.list_code.item(i).setSelected(True)
            
            
    @pyqtSlot(int)
    def highlight_instruction(self, pc):
        print(pc)
        for i, line in enumerate(self.code_lbls):
            if line['pc'] == pc:
                item = self.list_code.item(i)
                item.setSelected(True)
                self.list_code.scrollToItem(item)
            else:
                item = self.list_code.item(i)
                item.setSelected(False)
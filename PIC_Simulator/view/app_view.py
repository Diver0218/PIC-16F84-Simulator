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
    sig_update_bit = pyqtSignal(list)

    def __init__(self, rows, columns, parent):
        QTableWidget.__init__(self, rows, columns, parent)
        self.sig_update_bit.connect(parent.update_single_register_bit)
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
                    newitem = QTableWidgetItem(f"{item:02x}".upper())
                    self.setItem(i , j, newitem)
                else:
                    item = mem.get_bank_specific_register(i, 0).test_bit(7-j)
                    newitem = QTableWidgetItem(str(item))
                    self.setItem(i , j, newitem)
            verticaHeaders.append(str(hex(i)).upper()[2:])
        self.setVerticalHeaderLabels(verticaHeaders)

    
    def setPortData(self, mem, adr):
        columns = self.columnCount()
        for i in range(columns):
            tbl_button = TblPortButton(adr, 7-i, self)
            tbl_button.setText(str(mem.get_bank_specific_register(adr, 0).test_bit(7 - i)))
            self.setCellWidget(2, i, tbl_button)
        for i in range(columns):
            item = mem.get_bank_specific_register(adr, 1).test_bit(7 - i)
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
    
    @pyqtSlot(list)
    def signal_update_bit(self, update):
        self.sig_update_bit.emit(update)
            
class TblPortButton(QPushButton):
    sig_update_bit = pyqtSignal(list)
    port = 0
    bit = 0

    def __init__(self, n_port, n_bit, parent):
        super(TblPortButton, self).__init__(parent)
        self.port = n_port
        self.bit = n_bit
        self.sig_update_bit.connect(parent.signal_update_bit)
        self.clicked.connect(self.toggleButton)
        
    def toggleButton(self): #Muss noch mit Memory verbunden werden
        update = [self.port, self.bit]
        if self.text() == '1':
            self.setText('0')
            update.append(0)
        else:
            self.setText('1')
            update.append(1)
        self.sig_update_bit.emit(update)
        
    
class MainWindow(QMainWindow):
    
    sig_steprequest = pyqtSignal(bool)
    sig_init = pyqtSignal(bool)
    sig_update_register_bit = pyqtSignal(list)
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
        self.widg_reg = QWidget(self.widg_main)
        self.lay_reg = QVBoxLayout(self.widg_reg)
        self.tbl_porta = MemTable(3, 8, self)
        self.tbl_portb = MemTable(3, 8, self)
        self.tbl_mem = MemTable(80, 9, self)
        
        self.widg_sfr = QWidget(self.widg_reg)
        self.lay_sfr = QHBoxLayout(self.widg_sfr)
        self.lbl_Stack = QLabel(self.widg_sfr)
        
        self.widg_sfr_ou = QWidget(self.widg_sfr)
        self.lay_sfr_ou = QVBoxLayout(self.widg_sfr_ou)
        
        self.widg_sfr_vis_hid = QWidget(self.widg_sfr_ou)
        self.lay_sfr_vis_hid = QHBoxLayout(self.widg_sfr_vis_hid)
        
        self.widg_sfr_vis = QWidget(self.widg_sfr_vis_hid)
        self.lay_sfr_vis = QVBoxLayout(self.widg_sfr_vis)
        self.lbl_W = QLabel(self.widg_sfr_vis)
        
        self.widg_sfr_hid = QWidget(self.widg_sfr_vis_hid)
        self.lay_sfr_hid = QVBoxLayout(self.widg_sfr_hid)
        self.lbl_SP = QLabel(self.widg_sfr_hid)
        
        self.widg_sfr_etc = QWidget(self.widg_sfr_ou)
        self.lay_sfr_etc = QVBoxLayout(self.widg_sfr_etc)
        self.lbl_status = QLabel(self.widg_sfr_etc)
        
        self.tbl_porta.setHorizontalHeaderLabels(['RA 7','RA 6','RA 5','RA 4','RA 3','RA 2','RA 1','RA 0'])
        self.tbl_porta.setVerticalHeaderLabels(['TRIS','i/o','RA'])
        self.tbl_porta.resizePorts()
        self.tbl_portb.setHorizontalHeaderLabels(['RB 7','RB 6','RB 5','RB 4','RB 3','RB 2','RB 1','RB 0'])
        self.tbl_portb.setVerticalHeaderLabels(['TRIS','i/o','RB'])
        self.tbl_portb.resizePorts()
        self.tbl_mem.setHorizontalHeaderLabels(['Bit 7', 'Bit 6', 'Bit 5', 'Bit 4', 'Bit 3', 'Bit 2', 'Bit 1', 'Bit 0', 'Value'])
        self.tbl_mem.resizeColumnsToContents()
        self.tbl_mem.resizeRowsToContents()
        self.tbl_mem.setFixedWidth(353)

        self.lay_sfr_vis.addWidget(self.W)

        self.lay_sfr_vis_hid.addWidget(self.lay_sfr_vis)
        self.lay_sfr_vis_hid.addWidget(self.lay_sfr_hid)

        self.lay_sfr_ou.addWidget(self.widg_sfr_vis_hid)
        self.lay_sfr_ou.addWidget(self.widg_sfr_etc)

        self.lay_sfr.addWidget(self.widg_sfr_ou)
        self.lay_sfr.addWidget(self.lbl_Stack)
        
        self.lay_reg.addWidget(self.tbl_porta)
        self.lay_reg.addWidget(self.tbl_portb)
        self.lay_reg.addWidget(self.tbl_mem)
        self.lay_reg.addWidget(self.widg_sfr)
        
        self.widg_reg.setFixedWidth(370)
        
        #Code
        self.widg_code = QWidget(self.widg_main)
        self.lay_code = QVBoxLayout(self.widg_code)
        self.list_code = QListWidget()
        # self.lbl_code = QLabel("lskdugaldkgjsdlgkjbasdjgkbsdjgdfgdGSDGsdds\nwefwefewfwefwefwefWEFWefWEGWegewG\n hfgduzsgkeriugziebsztieruztvgerzuvteuzteriuvziguzrgiuzrgkazgrzaergkzeragkreuz")

        self.lay_code.addWidget(self.list_code)
        
        #Run Control
        self.widg_runctrl = QWidget(self.widg_main)
        self.lay_runctrl = QVBoxLayout(self.widg_runctrl)
        
        self.widg_brk = QWidget(self.widg_runctrl)
        self.lay_brk = QHBoxLayout(self.widg_brk)
        
        self.widg_freq = QWidget(self.widg_runctrl)
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
        
        self.widg_runctrl.setFixedWidth(200)
        
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
        self.resize(1800, 1000)
        

    def init_window(self):
        self.create_window()
        self.show()
        self.tbl_mem.show()
        self.init_new_processor()

    @pyqtSlot(tuple)
    def setMemData(self, proc_data):
        #debug:
        #print("Funktion aufgerufen: setMemData")
        #enddebug
        self.tbl_mem.setData(proc_data[0])
        self.tbl_porta.setPortData(proc_data[0], 5)
        self.tbl_portb.setPortData(proc_data[0], 6)
        self.set_fsr(proc_data[0], proc_data[1])
    
    def set_fsr(self, mem:Memory, W):
        self.lbl_W.setText(f"W-Reg.: " + f"{W.value:02x}".upper())
        stack_str = ""
        for stack_part in mem.stack:
            stack_str += f"{stack_part:04x}\n".upper()
        self.lbl_Stack.setText(f"Stack: \n{stack_str}")
        self.lbl_SP.setText(f"SP: {mem.stackpointer}")

    @pyqtSlot()
    def btn_step_method(self):
        self.sig_steprequest.emit(True)
    
    @pyqtSlot(list)
    def update_single_register_bit(self, update):
        self.sig_update_register_bit.emit(update)
    
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
                print("No Thread to terminate")
            self.init_new_processor()
            self.show_Code(file)
            print(self.lst.get_instructions())
            
    def init_new_processor(self):
        self.p = Processor(self.lst.get_instructions())
        self.p.sig_mem.connect(self.setMemData)
        self.sig_steprequest.connect(self.p.step)
        self.p.sig_pc.connect(self.highlight_instruction)
        self.sig_init.connect(self.p.init_view)
        self.sig_update_register_bit.connect(self.p.update_single_register_bit)
        self.p.update_mem()
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
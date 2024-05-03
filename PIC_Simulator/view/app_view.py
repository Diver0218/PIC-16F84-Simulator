from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QMainWindow, QLayout, QFileDialog, QHeaderView, QCheckBox
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt6.QtGui import QColor
from control.processor import Processor
from lst_parser_bits import Listing
from model.memory import Memory
#debug
from PyQt6.QtWidgets import QDialog
from PyQt6 import QtGui
#enddebug

class MemTable(QTableWidget):
    sig_update_bit = pyqtSignal(list)
    toggled = False

    def __init__(self, rows, columns, parent):
        QTableWidget.__init__(self, rows, columns, parent)
        self.sig_update_bit.connect(parent.update_single_register_bit)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.itemChanged.connect(parent.update_input_mem)

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
                    item = TblPortButton(i, 7 - j, self)
                    item.setText(str(mem.get_bank_specific_register(i, 0).test_bit(7 - j)))
                    self.setCellWidget(i , j, item)
            verticaHeaders.append(str(hex(i)).upper()[2:])
        self.setVerticalHeaderLabels(verticaHeaders)

    
    def setPortData(self, mem:Memory, adr):
        columns = self.columnCount()
        for i in range(columns):
            item = mem.get_bank_specific_register(adr, 1).test_bit(7 - i)
            self.setItem(0, i, QTableWidgetItem(str(item))) # evtl hier auch ToggleButton einfügen
            tbl_button = TblPortButton(adr, 7-i, self)
            if item:
                self.setItem(1, i, QTableWidgetItem('i'))
            else:
                self.setItem(1, i, QTableWidgetItem('o'))
                tbl_button.setText(str(mem.data_latch[adr-5][7-i]))
                self.setCellWidget(2, i, tbl_button)    
            if self.toggled:
                tbl_button.setText(str(mem.data_latch[adr-5][7-i]))
                self.setCellWidget(2, i, tbl_button)    
        for i in range(columns):
            if not self.cellWidget(2, i):
                tbl_button = TblPortButton(adr, 7-i, self)
                self.setCellWidget(2, i, tbl_button)    
                self.cellWidget(2, i).setText('0')
        self.toggled = False

    def resizePorts(self):
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setFixedSize(354, 98)
    
    @pyqtSlot(list)
    def signal_update_bit(self, update):
        self.toggled = True
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
        
    def toggleButton(self):
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
    sig_reset_mem = pyqtSignal(bool)
    sig_update_input_mem = pyqtSignal(list)
    is_set_data = True
    sig_run = pyqtSignal(bool)
    code_lbls = []
    sig_frequenz = pyqtSignal(float)
    sig_wd_enabled = pyqtSignal(bool)
    breakpoints = []

    def __init__(self):
        super().__init__()
        self.lst = Listing("")
        self._running = False
        self.setWindowTitle("PIC-16F84 Simulator")

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
        self.but_reg_reset = QPushButton(self.widg_reg)
        self.tbl_porta = MemTable(3, 8, self)
        self.tbl_portb = MemTable(3, 8, self)
        self.tbl_mem = MemTable(80, 9, self)
        
        self.widg_sfr = QWidget(self.widg_reg)
        self.widg_sfr.setStyleSheet("QWidget { border: 1px solid black; }")
        self.lay_sfr = QHBoxLayout(self.widg_sfr)
        self.lbl_stack = QLabel(self.widg_sfr)
        
        self.widg_sfr_ou = QWidget(self.widg_sfr)
        self.lay_sfr_ou = QVBoxLayout(self.widg_sfr_ou)
        
        self.widg_sfr_vis_hid = QWidget(self.widg_sfr_ou)
        self.lay_sfr_vis_hid = QHBoxLayout(self.widg_sfr_vis_hid)
        
        self.widg_sfr_vis = QWidget(self.widg_sfr_vis_hid)
        self.lay_sfr_vis = QVBoxLayout(self.widg_sfr_vis)
        self.lbl_W = QLabel(self.widg_sfr_vis)
        self.lbl_fsr = QLabel(self.widg_sfr_vis)
        self.lbl_pcl = QLabel(self.widg_sfr_vis)
        self.lbl_pclath = QLabel(self.widg_sfr_vis)
        
        self.widg_sfr_hid = QWidget(self.widg_sfr_vis_hid)
        self.lay_sfr_hid = QVBoxLayout(self.widg_sfr_hid)
        self.lbl_pc = QLabel(self.widg_sfr_hid)
        self.lbl_sp = QLabel(self.widg_sfr_hid)
        
        self.widg_sfr_etc = QWidget(self.widg_sfr_ou)
        self.lay_sfr_etc = QVBoxLayout(self.widg_sfr_etc)
        self.lbl_status = QLabel(self.widg_sfr_etc)
        self.lbl_option = QLabel(self.widg_sfr_etc)
        self.lbl_intcon = QLabel(self.widg_sfr_etc)

        self.but_reg_reset.setText("Reset (MCLR)")
        self.but_reg_reset.clicked.connect(self.reset_mem)
        
        self.tbl_porta.setHorizontalHeaderLabels(['RA 7','RA 6','RA 5','RA 4','RA 3','RA 2','RA 1','RA 0'])
        self.tbl_porta.setVerticalHeaderLabels(['TRIS','i/o','Pin'])
        self.tbl_porta.resizePorts()
        self.tbl_portb.setHorizontalHeaderLabels(['RB 7','RB 6','RB 5','RB 4','RB 3','RB 2','RB 1','RB 0'])
        self.tbl_portb.setVerticalHeaderLabels(['TRIS','i/o','Pin'])
        self.tbl_portb.resizePorts()
        self.tbl_mem.setHorizontalHeaderLabels(['Bit 7', 'Bit 6', 'Bit 5', 'Bit 4', 'Bit 3', 'Bit 2', 'Bit 1', 'Bit 0', 'Value'])
        self.tbl_mem.resizeColumnsToContents()
        self.tbl_mem.resizeRowsToContents()
        self.tbl_mem.setFixedWidth(354)

        self.lay_sfr_vis.addWidget(self.lbl_W)
        self.lay_sfr_vis.addWidget(self.lbl_fsr)
        self.lay_sfr_vis.addWidget(self.lbl_pcl)
        self.lay_sfr_vis.addWidget(self.lbl_pclath)

        self.lay_sfr_hid.addWidget(self.lbl_pc)
        self.lay_sfr_hid.addWidget(self.lbl_sp)

        self.lay_sfr_vis_hid.addWidget(self.widg_sfr_vis)
        self.lay_sfr_vis_hid.addWidget(self.widg_sfr_hid)

        self.lay_sfr_etc.addWidget(self.lbl_status)
        self.lay_sfr_etc.addWidget(self.lbl_status)
        self.lay_sfr_etc.addWidget(self.lbl_status)
        self.lay_sfr_etc.addWidget(self.lbl_option)
        self.lay_sfr_etc.addWidget(self.lbl_intcon)

        self.lay_sfr_ou.addWidget(self.widg_sfr_vis_hid)
        self.lay_sfr_ou.addWidget(self.widg_sfr_etc)

        self.lay_sfr.addWidget(self.widg_sfr_ou)
        self.lay_sfr.addWidget(self.lbl_stack)
        self.widg_sfr.setFixedWidth(354)
        
        self.lay_reg.addWidget(self.but_reg_reset)
        self.lay_reg.addWidget(self.tbl_porta)
        self.lay_reg.addWidget(self.tbl_portb)
        self.lay_reg.addWidget(self.tbl_mem)
        self.lay_reg.addWidget(self.widg_sfr)
        
        self.widg_reg.setFixedWidth(370)
        
        #Code
        self.widg_code = QWidget(self.widg_main)
        self.lay_code = QVBoxLayout(self.widg_code)
        self.list_code = QListWidget()
        self.list_code.itemDoubleClicked.connect(self.toggle_breakpoint)

        self.lay_code.addWidget(self.list_code)
        
        #Run Control
        self.widg_runctrl = QWidget(self.widg_main)
        self.lay_runctrl = QVBoxLayout(self.widg_runctrl)
        
        self.widg_freq = QWidget(self.widg_runctrl)
        self.lay_freq = QHBoxLayout(self.widg_freq)

        self.widg_timer = QWidget(self.widg_runctrl)
        self.lay_timer = QHBoxLayout(self.widg_timer)
        
        self.widg_wd_timer = QWidget(self.widg_runctrl)
        self.lay_wd_timer = QVBoxLayout(self.widg_wd_timer)
        
        self.btn_step = QPushButton('Step')
        self.btn_run = QPushButton('Run')
        self.btn_stop = QPushButton('Stop')
        self.btn_reset = QPushButton('Reset')
        self.txtbox_brk = QLineEdit("-")
        self.txtbox_freq = QLineEdit("4.0")
        self.btn_setbrk = QPushButton('Set')
        self.lbl_timer = QLabel("Laufzeit: 0µs")
        self.lbl_freq = QLabel("Frequenz in MHz:")
        self.chbx_wd_timer = QCheckBox("Watchdog Timer aktiviert")
        self.lbl_wd_timer = QLabel("Watchdog Timer: 0µs")

        
        self.btn_step.clicked.connect(self.btn_step_method)
        self.btn_run.clicked.connect(self.run)
        self.btn_stop.clicked.connect(self.stop)
        self.chbx_wd_timer.stateChanged.connect(self.change_wd_enable)
        
        self.txtbox_freq.textChanged.connect(self.send_freq)
        
        self.lay_runctrl.addWidget(self.btn_step)
        self.btn_step.move(20, 20)
        self.lay_runctrl.addWidget(self.btn_run)
        self.lay_runctrl.addWidget(self.btn_stop)
        self.lay_runctrl.addWidget(self.btn_reset)
        
        self.lay_freq.addWidget(self.lbl_freq)
        self.lay_freq.addWidget(self.txtbox_freq)
        self.widg_freq.setMaximumHeight(40)

        self.lay_timer.addWidget(self.lbl_timer)
        self.widg_timer.setMaximumHeight(40)
        
        self.lay_wd_timer.addWidget(self.chbx_wd_timer)
        self.lay_wd_timer.addWidget(self.lbl_wd_timer)
        self.widg_wd_timer.setMaximumHeight(60)
        
        self.lay_runctrl.addWidget(self.widg_freq)
        self.lay_runctrl.addWidget(self.widg_timer)
        self.lay_runctrl.addWidget(self.widg_wd_timer)
        
        # self.widg_runctrl.setStyleSheet("QWidget { border: 1px solid black; }")
        self.widg_runctrl.setFixedWidth(200)
        self.widg_runctrl.setMaximumHeight(330)
        
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
        self.is_set_data = True
        self.tbl_mem.setData(proc_data[0])
        self.tbl_porta.setPortData(proc_data[0], 5)
        self.tbl_portb.setPortData(proc_data[0], 6)
        self.set_fsr(proc_data[0], proc_data[1])
        self.is_set_data = False
    
    def set_fsr(self, mem:Memory, W):
        #vis
        self.lbl_W.setText(f"W-Reg.:            " + f"{W.value:02x}".upper())
        self.lbl_fsr.setText(f"FSR:                  " + f"{mem[4].value:02x}".upper())
        self.lbl_pcl.setText(f"PCL:                  " + f"{mem[2].value:02x}".upper())
        self.lbl_pclath.setText(f"PCLATH:           " + f"{mem[10].value:02x}".upper())
        #hid
        self.lbl_pc.setText(f"PC:                {mem.pc:04x}")
        self.lbl_sp.setText(f"SP:                      {mem.stackpointer}")
        #etc
        self.lbl_status.setText(f"Status: {mem[3].value:02x}    \nIRP:  RP1:    RP0:    TO:     PD:     Z:      DC:     C:\n{mem[3].test_bit(7)}      {mem[3].test_bit(6)}         {mem[3].test_bit(5)}         {mem[3].test_bit(4)}        {mem[3].test_bit(3)}         {mem[3].test_bit(2)}       {mem[3].test_bit(1)}         {mem[3].test_bit(0)}")
        self.lbl_option.setText(f"Option: {mem[0x81].value:02x}\nRBP:  IntEdg: T0CS: T0SE:  PSA:  PS2:  PS1:  PS0:\n{mem[0x81].test_bit(7)}       {mem[0x81].test_bit(6)}           {mem[0x81].test_bit(5)}       {mem[0x81].test_bit(4)}         {mem[0x81].test_bit(3)}       {mem[0x81].test_bit(2)}       {mem[0x81].test_bit(1)}       {mem[0x81].test_bit(0)}")
        self.lbl_intcon.setText(f"INTCON: {mem[0x0B].value:02x}\nGIE:  EEIE:  T0IE:  INTE:  RBIE:  T0IF:  INTF:  RBIF:\n{mem[0x0B].test_bit(7)}      {mem[0x0B].test_bit(6)}        {mem[0x0B].test_bit(5)}       {mem[0x0B].test_bit(4)}         {mem[0x0B].test_bit(3)}        {mem[0x0B].test_bit(2)}       {mem[0x0B].test_bit(1)}        {mem[0x0B].test_bit(0)}")
        #stack
        stack_str = ""
        for stack_part in mem.stack:
            stack_str += f"{stack_part:04x}\n".upper()
        self.lbl_stack.setText(f"Stack: \n{stack_str}")

    @pyqtSlot(QTableWidgetItem)
    def update_input_mem(self, item:QTableWidgetItem):
        if item.column() == 8 and not self.is_set_data:
            self.sig_update_input_mem.emit([item.row(), int(item.text(), 16)])
        
    @pyqtSlot()
    def btn_step_method(self):
        self.sig_steprequest.emit(True)

    @pyqtSlot()
    def reset_mem(self):
        self.sig_reset_mem.emit(True)
    
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
                self.p_thread.quit()
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
        self.sig_reset_mem.connect(self.p.mclr_reset)
        self.sig_update_input_mem.connect(self.p.update_table_input_mem)
        self.sig_run.connect(self.p.run_instructions)
        self.p.sig_continue.connect(self.continue_run)
        self.p.sig_runtime.connect(self.set_runtime)
        self.sig_frequenz.connect(self.p.set_freq)
        self.sig_wd_enabled.connect(self.p.set_wd_enabled)
        self.p.sig_Watchdog_Timer.connect(self.set_wd_timer_text)
        self.sig_frequenz.emit(float(self.txtbox_freq.text()))
        self.p.update_mem()
        self.p_thread = QThread()
        self.p.moveToThread(self.p_thread)
        self.p_thread.start()
        self.lbl_timer.setText("Laufzeit: 0µs")
        self.lbl_wd_timer.setText(f"Watchdog Timer: 0µs")
        self.change_wd_enable()
        self.breakpoints = []

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
        for i, line in enumerate(self.code_lbls):
            if line['pc'] == pc:
                item = self.list_code.item(i)
                item.setSelected(True)
                self.list_code.scrollToItem(item)
            else:
                item = self.list_code.item(i)
                item.setSelected(False)
                
    @pyqtSlot()
    def run(self):
        self._running = True
        self.sig_run.emit(self._running)
        
    @pyqtSlot()
    def stop(self):
        self._running = False
    
    @pyqtSlot(bool)
    def continue_run(self):
        if self.p.mem.pc in self.breakpoints:
            self.stop()
        self.sig_run.emit(self._running)
    
    @pyqtSlot(int)
    def set_runtime(self, cycles):
        self.lbl_timer.setText(f"Laufzeit: {round(cycles/float(self.txtbox_freq.text()), 3)*4}µs")
     
    @pyqtSlot(int)   
    def change_wd_enable(self):
        self.sig_wd_enabled.emit(self.chbx_wd_timer.isChecked())
        
    @pyqtSlot(float)
    def set_wd_timer_text(self, time:float):
        self.lbl_wd_timer.setText(f"Watchdog Timer: {round(time, 2)}µs")
        
    @pyqtSlot(str)
    def send_freq(self):
        try:
            self.sig_frequenz.emit(float(self.txtbox_freq.text()))
        except:
            self.sig_frequenz.emit(0.0)


    @pyqtSlot(QListWidgetItem)
    def toggle_breakpoint(self, item:QListWidgetItem):
        entry = next(entry for entry in self.code_lbls if entry['label'] == item)
        if item.foreground().color() == QColor("red"):
            item.setForeground(QColor("black"))
            self.breakpoints.remove(entry['pc'])
        else:
            item.setForeground(QColor("red"))
            self.breakpoints.append(entry["pc"])

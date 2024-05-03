from .registers import Register
from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
import debugpy

class Memory(QObject):

    # Bank 0
    # INDF : Register
    # TMR0 : Register
    # PCL : Register
    # STATUS : Register
    # FSR : Register
    # PORTA : Register
    # PORTB : Register
    # EEDATA : Register
    # EEADR : Register
    # PCLATH : Register
    # INTCON : Register

    # # Bank 1
    # OPTION_REG : Register
    # TRISA : Register
    # TRISB : Register
    # EECON1 : Register
    # EECON2 : Register
    
    sig_timer0_set = pyqtSignal(bool)
    sig_pclath = pyqtSignal(bool)
    data_latch = [int(0) for _ in range(2)]
    eeprom = [[Register(0) for _ in range(80)] for _ in range(2)]

    def __init__(self):
        super().__init__()
        self.eeprom = [[Register(0, self) for _ in range(80)] for _ in range(2)]
        self.stackpointer : int = 0
        self.stack : list[int] = [int(0) for _ in range(8)] 
        self.pc : int = 0   
        self.bank_relevant_adr = [0x01, 0x05, 0x06, 0x08, 0x09]
        self.data_latch = [[int(0) for _ in range(8)] for _ in range(2)]
        self.power_reset()

    def __str__(self):
        retValue = ""
        bank0 = self.eeprom[0]
        bank1 = self.eeprom[1]
        for index in range(len(bank0)):
            retValue += f"Adresse: {index:02X}, Bank 0: {str(bank0[index])}, Bank 1: {str(bank1[index])}'\n'"
        return retValue
    
    def __setitem__(self, index, value):
        tuple_index = self._handle_index(index)
        if tuple_index == [1, 0]:
            self.sig_timer0_set.emit(True)
        if (self.eeprom[0][3].test_bit(5) and index in self.bank_relevant_adr) or tuple_index[1]:
            self.eeprom[1][tuple_index[0]].set(value)
        else:
            self.eeprom[0][tuple_index[0]].set(value)
        if tuple_index == [2, 0]:
            self.sig_pclath.emit(True) 
        if tuple_index == [5, 0] or tuple_index == [6, 0]:
            for i in range(8):
                self.data_latch[tuple_index[0]-5][i] = self.eeprom[0][tuple_index[0]].test_bit(i)

    def __getitem__(self, index):
        tuple_index = self._handle_index(index)
        if (self.eeprom[0][3].test_bit(5) and index in self.bank_relevant_adr) or tuple_index[1]:
            return self.eeprom[1][tuple_index[0]]    
        else:
            return self.eeprom[0][tuple_index[0]] 

    def get_bank_specific_register(self, index, bank):
        if bank and index in self.bank_relevant_adr:
            return self.eeprom[1][index]    
        else:
            return self.eeprom[0][index]
    
    def _handle_index(self, index):
        if index == 0:
            return [self.eeprom[0][4].value, 0]   
        if index < 80:
            return [index, 0]
        elif index < 128:
            return [-1, 0]
        elif index < 208:
            if index - 128 in self.bank_relevant_adr:
                return [index - 128, 1]
            else:
                return [index - 128, 0]
                    
    def inc_pc(self, amount : int = 1):
        if self.pc < 8192:
            self.pc += amount
        else:
            self.pc = 0
        print(f"PC: {self.pc}")

    def set_pc(self, pc):
        self.pc = pc

    def push_pc(self):
        if self.stackpointer >= 7:
            self.stack[self.stackpointer] = self.pc + 1
            self.stackpointer = 0
        else:
            self.stack[self.stackpointer] = self.pc + 1
            self.stackpointer += 1

    def pop_pc(self):
        if self.stackpointer <= 0:
            self.stackpointer = 7
            retAdr = self.stack[self.stackpointer]
        else:
            self.stackpointer -= 1
            retAdr = self.stack[self.stackpointer]
        return retAdr
    
    def reset(self, type:str):
        debugpy.debug_this_thread()
        for item in self.eeprom[0][0xc:]:
            item.set(0)
        self[2].set(0)
        self.pc = 0
        self[3] = self[3] & 0b00011111
        self[0xA].set(0)
        self[0xB] = self[0xB] & 0b00000001
        self[0x81].set(0b11111111)
        self[0x85].set(0b00011111)
        self[0x86].set(0b11111111)
        self[0x88] = self[0x88] & 0b00001000
            
    def increment_timer0(self):
        self.eeprom[0][1].value += 1

    def power_reset(self):
        self.pc = 0
        self[0x02] = 0
        self[0x03] = (self[3] & 0b00000111) | 0b00011000
        self[0x0A] = 0
        self[0x0B] = self[0xB] & 0b00000001
        self[0x81] = 0b11111111
        self[0x85] = 0b00011111
        self[0x86] = 0b11111111
        self[0x88] = self[3] & 0b00001000

    @pyqtSlot(object)
    def set_data_latch(self, reg):
        reg_adr = self.compare_regs(reg)
        if reg_adr[1] in [5, 6] and reg_adr[0] == 0:
            for i in range(8):
                self.data_latch[reg_adr[1]-5][i] = self.eeprom[0][reg_adr[1]].test_bit(i)
    
    def compare_regs(self, reg):
        bank_index = 0
        reg_index = 0
        for bank in self.eeprom:
            for regis in bank:
                if regis is reg:
                    return [bank_index, reg_index]
                reg_index += 1
            bank_index += 1
        return [-1, -1]

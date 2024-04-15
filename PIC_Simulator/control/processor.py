from model.memory import Memory
from model.registers import W_Register
from PyQt6.QtCore import QObject

STATUS = 0x03
Z = 2
C = 0
DC = 1

class Processor(QObject):

    mem = Memory()
    W = W_Register(0)
    quartz = int()
    inst = list()

    def __init__(self, inst) -> None:
        super().__init__()
        self.inst = inst
        self.mem.inc_pc()

    def addlw(self, k):
        self.W += k
        self.carry_flag(self.W)
        self.zero_flag(self.W)
        self.mem.inc_pc()

    def andlw(self, k):
        self.W &= k
        self.zero_flag(self.W)
        self.mem.inc_pc()

    def addwf(self, f, d = 0):
        if d == 0:
            self.W += self.mem[f]
            self.carry_flag(self.W)
            self.zero_flag(self.W)
        else:
            self.mem.eeprom[f] += self.W
            self.carry_flag(self.mem[f])
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()

    def andwf(self, f, d = 0):
        if d == 0:
            self.W &= self.mem[f]
            self.zero_flag(self.W)
        else:
            self.mem[f] &= self.W
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()

    def bcf(self, f, b):
        if f == 'W':
            self.W.set_bit(b, 0)
        else:
            self.mem[f].set_bit(b, 0)
        self.mem.inc_pc()

    def btfsc(self, f, b):
        if f == 'W':
            if not self.W.test_bit(b):
                self.mem.inc_pc()
        else:
            if not self.mem[f].test_bit(b):
               self.mem.inc_pc()
        self.mem.inc_pc()

    def bsf(self, f, b):
        if f == 'W':
            self.W.set_bit(b, 1)
        else:
            self.mem[f].set_bit(b, 1)
        self.mem.inc_pc()

    def btfss(self, f, b):
        if f == 'W':
            if self.W.test_bit(b):
                self.mem.inc_pc()
        else:
            if self.mem[f].test_bit(b):
               self.mem.inc_pc()
        self.mem.inc_pc()

    def call(self, k):
        self.mem.push_pc()
        self.mem.set_pc(k)
        return
    
    def clrf(self, f):
        self.mem[f].set(0x00)
        self.zero_flag(self.mem[f])
        self.mem.inc_pc()

    def clrw(self):
        self.W.set(0x00)
        self.zero_flag(self.W)
        self.mem.inc_pc()

    def clrwdt(self):
        #clear watch dog timer Routine
        return
    
    def comf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(~self.mem[f])
            self.zero_flag(self.W)
        else:
            self.mem[f] = ~self.mem[f]
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()

    def decfsz(self, f, d = 0):
        if d == 0:
            self.mem[f] = self.mem[f].decrement()
        else:
            self.W = W_Register(self.mem[f].decrement())
        if self.mem[f] == 0:
            self.nop()
        self.mem.inc_pc()

    def decf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(self.mem[f].decrement())
            self.zero_flag(self.W)
        else:
            self.mem[f] = self.mem[f].decrement()
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()

    def goto(self, k):
        self.mem.set_pc(k)
        return
    
    def incf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(self.mem[f].increment())
            self.zero_flag(self.W)
        else:
            self.mem[f] = self.mem[f].increment()
            self.zero_flag(self.mem[f])

    def incfsz(self, f, d = 0):
        if d == 0:
            self.mem[f] = self.mem[f].increment()
        else:
            self.W = W_Register(self.mem[f].increment())
        if self.mem[f] == 0:
            self.nop()
        self.mem.inc_pc()

    def iorlw(self, k):
        self.W |= k
        self.zero_flag(self.W)
        self.mem.inc_pc()

    def iorwf(self, f, d  = 0):
        if d == 0:
            self.W |= self.mem[f]
            self.zero_flag(self.W)
        else:
            self.mem[f] |= self.W
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()

    def movlw(self, k):
        self.W.set(k)
        self.mem.inc_pc()

    def movf(self, f, d = 0):
        if d == 0:
            self.W.set(self.mem[f])
            self.zero_flag(self.W)
        else:
            self.mem[f].set(self.mem[f])
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()
               
    def movwf(self, f):
        self.mem[f] = self.W
        self.mem.inc_pc()
    
    def nop(self):
        self.mem.inc_pc()
    
    def retfie(self):
        # Return from Interrupt
        return
    
    def retlw(self, k):
        self.W.set(k)
        self.mem.set_pc(self.mem.pop_pc())
        return
    
    def _return(self):
        self.mem.set_pc(self.mem.pop_pc())
        return
    
    def rlf(self, f, d = 0):
        carry_tmp = self.mem[STATUS].test_bit(C)
        self.carry_flag_rotate(self.mem[f], 7)
        if d == 0:
            self.W = W_Register(self.mem[f] << 1)
            self.W.set_bit(0, carry_tmp)
        else:
            self.mem[f] <<= 1
            self.mem[f].set_bit(0, carry_tmp)
        self.mem.inc_pc()

    def rrf(self, f, d = 0):
        carry_tmp = self.mem[STATUS].test_bit(C)
        self.carry_flag_rotate(self.mem[f], 0)
        if d == 0:
            self.W = W_Register(self.mem[f] >> 1)
            self.W.set_bit(7, carry_tmp)
        else:
            self.mem[f] >>= 1
            self.W.set_bit(7, carry_tmp)
        self.mem.inc_pc()

    def sleep(self):
        # Sleep Routine
        return
    
    def sublw(self, k):
        self.W -= k
        self.carry_flag(self.W)
        self.zero_flag(self.W)
        self.mem.inc_pc()

    def subwf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(-(self.W -self.mem[f]))
            self.carry_flag(self.W)
            self.zero_flag(self.W)
        else:
            self.mem[f] -= self.W
            self.carry_flag(self.mem[f])
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()

    def swapf(self, f, d = 0):
        # Swap Nibbles in f
        return
    
    def xorlw(self, k):
        self.W ^= k
        self.zero_flag(self.W)
        self.mem.inc_pc()

    def xorwf(self, f, d = 0):
        if d == 0:
            self.W ^= self.mem[f]
            self.zero_flag(self.W)
        else:
            self.mem[f] ^= self.W
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()

    def carry_flag(self, reg):
        if reg.value > 0xFF:
            reg.set(reg % 0xFF)
            self.mem[STATUS].set_bit(C, 1)
    
    def carry_flag_rotate(self, reg, bit):
        self.mem[STATUS].set_bit(C, reg.test_bit(bit))

    def zero_flag(self, reg):
        if reg.value == 0:
            reg.set_bit(Z, 1)
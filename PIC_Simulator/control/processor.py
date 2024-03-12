from model.memory import Memory
from model.registers import W_Register

class Processor():

    mem = Memory()
    W = W_Register(0)
    quartz = int()
    inst = list()
    JPS = list()

    def __init__(self, inst, JPs) -> None:
        self.inst = inst
        self.JPs = JPs
        self.mem.inc_pc()

    def addlw(self, k):
        self.W += k
        self.mem.inc_pc()

    def andlw(self, k):
        self.W &= k
        self.mem.inc_pc()

    def addwf(self, f, d = 0):
        if d == 0:
            self.W += self.mem.eeprom[f]
        else:
            self.mem.eeprom[f] += self.W
        self.mem.inc_pc()

    def andwf(self, f, d = 0):
        if d == 0:
            self.W &= self.mem.eeprom[f]
        else:
            self.mem.eeprom[f] &= self.W
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
        #call Routine
        return
    
    def clrf(self, f):
        self.mem[f].set(0x00)
        self.mem.inc_pc()

    def clrw(self):
        self.W.set(0x00)
        self.mem.inc_pc()

    def clrwdt(self):
        #clear watch dog timer Routine
        return
    
    def comf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(~self.mem[f])
        else:
            self.mem[f] = ~self.mem[f]
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
        else:
            self.mem[f] -= 1
        self.mem.inc_pc()

    def goto(self, k):
        #goto Routine
        return
    
    def incf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(self.mem[f].increment())
        else:
            self.mem[f] = self.mem[f].increment()

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
        self.mem.inc_pc()

    def iorwf(self, f, d  = 0):
        if d == 0:
            self.W |= self.mem[f]
        else:
            self.mem[f] |= self.W
        self.mem.inc_pc()

    def movlw(self, k):
        self.W.set(k)
        self.mem.inc_pc()

    def movf(self, f, d = 0):
        if d == 0:
            self.W.set(self.mem[f])
        else:
            self.mem[f].set(self.mem[f])
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
        # Return literal to W
        return
    
    def _return(self):
        # Return
        return
    
    def rlf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(self.mem[f] << 1)
        else:
            self.mem[f] <<= 1
        self.mem.inc_pc()

    def rrf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(self.mem[f] >> 1)
        else:
            self.mem[f] >>= 1
        self.mem.inc_pc()

    def sleep(self):
        # Sleep Routine
        return
    
    def sublw(self, k):
        self.W -= k
        self.mem.inc_pc()

    def subwf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(-(self.W -self.mem[f]))
        else:
            self.mem[f] -= self.W
        self.mem.inc_pc()

    def swapf(self, f, d = 0):
        # Swap Nibbles in f
        return
    
    def xorlw(self, k):
        self.W ^= k
        self.mem.inc_pc()

    def xorwf(self, f, d = 0):
        if d == 0:
            self.W ^= self.mem[f]
        else:
            self.mem[f] ^= self.W
        self.mem.inc_pc()
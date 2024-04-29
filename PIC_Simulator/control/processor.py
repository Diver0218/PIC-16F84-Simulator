from model.memory import Memory
from model.registers import W_Register, Register
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
#debug
from PyQt6.QtWidgets import QDialog
import debugpy, time
#enddebug

STATUS = 0x03
Z = 2
C = 0

DC = 1

class Processor(QThread):

    mem = Memory()
    W = W_Register(0)
    quartz = int()
    inst = list()
    
    sig_mem = pyqtSignal(tuple)
    sig_quartz = pyqtSignal(int)
    sig_inst = pyqtSignal(list)
    sig_pc = pyqtSignal(int)

    def __init__(self, inst) -> None:
        super().__init__()
        self.inst = inst
        self.mem.__init__()
        self.mem.pc = 0
        self.update_pc()
        self.update_mem()
        self._running = False
        
        
    # def set_instructions(self, inst):
    #     self.inst = inst
    #     self.mem.inc_pc()
    #     self.update_inst(inst)
            
#region Instructions
    def addlw(self, k):
        self.digit_carry_flag_add(self.W, k)
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
            self.digit_carry_flag_add(self.W, self.mem[f])
            self.W += self.mem[f]
            self.carry_flag(self.W)
            self.zero_flag(self.W)
        else:
            self.mem[f] += self.W
            self.digit_carry_flag_add(self.mem[f], self.W)
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
        self.mem[f].set_bit(b, 0)
        self.mem.inc_pc()

    def btfsc(self, f, b):
        if not self.mem[f].test_bit(b):
            self.mem.inc_pc()
        self.mem.inc_pc()

    def bsf(self, f, b):
        self.mem[f].set_bit(b, 1)
        self.mem.inc_pc()

    def btfss(self, f, b):
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
        if d == 1:
            self.mem[f] = self.mem[f].decrement()
            if self.mem[f] & 0xFF == 0:
                self.mem.inc_pc()
        else:
            self.W = W_Register(self.mem[f].decrement())
            if self.W & 0xFF == 0:
                print("is zero")
                self.mem.inc_pc()
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
        self.mem.inc_pc()

    def incfsz(self, f, d = 0):
        if d == 1:
            self.mem[f] = self.mem[f].increment()
            if self.mem[f] & 0xFF == 0:
                self.mem.inc_pc()
        else:
            self.W = W_Register(self.mem[f].increment())
            if self.W & 0xFF == 0:
                self.mem.inc_pc()
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
        self.mem[f] = Register(self.W)
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
            self.W = W_Register((self.mem[f] << 1) & 0xFF)
            self.W.set_bit(0, carry_tmp)
        else:
            self.mem[f] <<= 1
            self.mem[f] &= 0xFF
            self.mem[f].set_bit(0, carry_tmp)
        self.mem.inc_pc()

    def rrf(self, f, d = 0):
        carry_tmp = self.mem[STATUS].test_bit(C)
        self.carry_flag_rotate(self.mem[f], 0)
        if d == 0:
            self.W = W_Register((self.mem[f] >> 1) & 0xFF)
            self.W.set_bit(7, carry_tmp)
        else:
            self.mem[f] >>= 1
            self.mem[f] &= 0xFF
            self.mem[f].set_bit(7, carry_tmp)
        self.mem.inc_pc()

    def sleep(self):
        # Sleep Routine
        return
    
    def sublw(self, k):
        self.digit_carry_flag_sub(self.W, k)
        self.W = W_Register(k - self.W.value)
        self.carry_flag_sub(self.W)
        self.zero_flag(self.W)
        self.mem.inc_pc()

    def subwf(self, f, d = 0):
        if d == 0:
            self.digit_carry_flag_sub(self.W, self.mem[f])
            self.W = W_Register(self.mem[f] - self.W)
            self.carry_flag_sub(self.W)
            self.zero_flag(self.W)
        else:
            self.digit_carry_flag_sub(self.W, self.mem[f])
            self.mem[f] = Register(self.mem[f] - self.W)
            self.carry_flag_sub(self.mem[f])
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()

    def swapf(self, f, d = 0):
        higher = (self.mem[f].value & 0xF0) >> 4
        lower = self.mem[f].value & 0x0F
        self.mem[f] = Register((lower << 4) + higher)
        self.mem.inc_pc()
    
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
#endregion

    def carry_flag(self, reg):
        if reg.value > 0xFF:
            reg.set(reg & 0xFF)
            self.mem[STATUS].set_bit(C, 1)
        else:
            reg.set(reg & 0xFF)
            self.mem[STATUS].set_bit(C, 0)
    
    def carry_flag_sub(self, reg):
        if reg.value >= 0:
            self.mem[STATUS].set_bit(C, 1)
            reg.set(reg & 0xFF)
        else:
            self.mem[STATUS].set_bit(C, 0)
            reg.set(reg & 0xFF)
    
    def carry_flag_rotate(self, reg, bit):
        self.mem[STATUS].set_bit(C, reg.test_bit(bit))

    def zero_flag(self, reg):
        if reg.value == 0:
            self.mem[STATUS].set_bit(Z, 1)
        else:
            self.mem[STATUS].set_bit(Z, 0)
            
    def digit_carry_flag_add(self, reg, k):
        masked_reg = reg.value & 0x0F
        if isinstance(k, Register):
            masked_k = k.value & 0x0F
        else:
            masked_k = k & 0x0F
        if masked_reg + masked_k > 0x0F:
            self.mem[STATUS].set_bit(DC, 1)
        else:
            self.mem[STATUS].set_bit(DC, 0)

    def digit_carry_flag_sub(self, reg, k):
        masked_reg = reg.value & 0x0F
        if isinstance(k, Register):
            masked_k = k.value & 0x0F
        else:
            masked_k = k & 0x0F
        if masked_k - masked_reg >= 0 and masked_k - masked_reg <= 0x0F:
            self.mem[STATUS].set_bit(DC, 1)
        else:
            self.mem[STATUS].set_bit(DC, 0)
            
    def update_mem(self):
        self.sig_mem.emit((self.mem, self.W))
        
    def update_quartz(self):
        self.sig_quartz.emit(self.quartz)
        
    def update_inst(self, inst):
        self.sig_inst.emit(self.inst)
        
    def update_pc(self):
        self.sig_pc.emit(self.mem.pc)
        
    @pyqtSlot(bool)
    def run(self):
        self._running = True
        while self._running == True:
            self.step()
            if self.isInterruptionRequested():
                self._running == False
            
        
    @pyqtSlot(bool)
    def step(self):
        debugpy.debug_this_thread()
        self.execute_instruction()
        self.update_mem()
        self.update_pc()
        #debug
        #print("Processor: Funktion aufgerufen: step")
        #enddebug
        
    @pyqtSlot(bool)
    def init_view(self):
        self.update_mem()
        self.update_quartz()
        self.update_inst(self.inst)
        self.update_pc()

    @pyqtSlot(list)
    def update_single_register_bit(self, update):
        debugpy.debug_this_thread()
        self.mem[update[0]].set_bit(update[1], update[2])
        self.update_mem()
           
    def execute_instruction(self):
        inst = self.inst[self.mem.pc]
        print("\n")
        print(inst)
        match inst['inst']:
            case 'addlw':
                self.addlw(inst['literal'])
            case 'andlw':
                self.andlw(inst['literal'])
            case 'addwf':
                self.addwf(inst['file'], inst['destination'])
            case 'andwf':
                self.andwf(inst['file'], inst['destination'])
            case 'bcf':
                self.bcf(inst['file'], inst['bit'])
            case 'btfsc':
                self.btfsc(inst['file'], inst['bit'])
            case 'bsf':
                self.bsf(inst['file'], inst['bit'])
            case 'btfss':
                self.btfss(inst['file'], inst['bit'])
            case 'call':
                self.call(inst['literal'])
            case 'clrf':
                self.clrf(inst['file'])
            case 'clrw':
                self.clrw()
            case 'clrwdt':
                self.clrwdt()
            case 'comf':
                self.comf(inst['file'], inst['destination'])
            case 'decfsz':
                self.decfsz(inst['file'], inst['destination'])
            case 'decf':
                self.decf(inst['file'], inst['destination'])
            case 'goto':
                self.goto(inst['literal'])
            case 'incf':
                self.incf(inst['file'], inst['destination'])
            case 'incfsz':
                self.incfsz(inst['file'], inst['destination'])
            case 'iorlw':
                self.iorlw(inst['literal'])
            case 'iorwf':
                self.iorwf(inst['file'], inst['destination'])
            case 'movlw':
                self.movlw(inst['literal'])
            case 'movf':
                self.movf(inst['file'], inst['destination'])
            case 'movwf':
                self.movwf(inst['file'])
            case 'nop':
                self.nop()
            case 'retfie':
                self.retfie()
            case 'retlw':
                self.retlw(inst['literal'])
            case 'return':
                self._return()
            case 'rlf':
                self.rlf(inst['file'], inst['destination'])
            case 'rrf':
                self.rrf(inst['file'], inst['destination'])
            case 'sleep':
                self.sleep()
            case 'sublw':
                self.sublw(inst['literal'])
            case 'subwf':
                self.subwf(inst['file'], inst['destination'])
            case 'swapf':
                self.swapf(inst['file'], inst['destination'])
            case 'xorlw':
                self.xorlw(inst['literal'])
            case 'xorwf':
                self.xorwf(inst['file'], inst['destination'])
            case _:
                pass
            
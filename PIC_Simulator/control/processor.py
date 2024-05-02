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

class Processor(QObject):

    mem = Memory()
    W = W_Register(0)
    quartz = int()
    inst = list()
    
    sig_mem = pyqtSignal(tuple)
    sig_updated_value_mem = pyqtSignal(Memory)
    sig_quartz = pyqtSignal(int)
    sig_inst = pyqtSignal(list)
    sig_pc = pyqtSignal(int)
    sig_continue = pyqtSignal(bool)
    sig_runtime = pyqtSignal(int)
    sig_Watchdog_Timer = pyqtSignal(float)

    def __init__(self, inst) -> None:
        super().__init__()
        self.inst = inst
        self.mem.__init__()
        self.mem.pc = 0
        self.update_pc()
        self.update_mem()
        self.Vorteiler_count = 0
        self.cycle : int = 0
        self.mem.sig_timer0_set.connect(self.handle_Timer0_changed)
        self.mem.sig_pclath.connect(self.handle_pclath)
        self.Timer0_changed = 0
        self.inst_pcl_set = False
        self.Watchdog_Timer:float = 0
        self.Watchdog_enabled = False
        
        
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
        self.inc_cycle()

    def andlw(self, k):
        self.W &= k
        self.zero_flag(self.W)
        self.mem.inc_pc()
        self.inc_cycle()

    def addwf(self, f, d = 0):
        if d == 0:
            self.digit_carry_flag_add(self.W, self.mem[f])
            self.W += self.mem[f]
            self.carry_flag(self.W)
            self.zero_flag(self.W)
        else:
            self.digit_carry_flag_add(self.mem[f], self.W)
            self.mem[f] += self.W
            self.carry_flag(self.mem[f])
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()
        self.inc_cycle()

    def andwf(self, f, d = 0):
        if d == 0:
            self.W &= self.mem[f]
            self.zero_flag(self.W)
        else:
            self.mem[f] &= self.W
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()
        self.inc_cycle()

    def bcf(self, f, b):
        self.mem[f].set_bit(b, 0)
        self.mem.inc_pc()
        self.inc_cycle()

    def btfsc(self, f, b):
        if not self.mem[f].test_bit(b):
            self.mem.inc_pc()
        self.mem.inc_pc()
        self.inc_cycle()

    def bsf(self, f, b):
        self.mem[f].set_bit(b, 1)
        self.mem.inc_pc()
        self.inc_cycle()

    def btfss(self, f, b):
        if self.mem[f].test_bit(b):
            self.mem.inc_pc()
        self.mem.inc_pc()
        self.inc_cycle()

    def call(self, k):
        self.mem.push_pc()
        pclath43 = (self.mem[0xA].value & 0b11000) << 8
        self.mem.set_pc(k+pclath43)
        self.inc_cycle(2)
        return
    
    def clrf(self, f):
        self.mem[f].set(0x00)
        self.zero_flag(self.mem[f])
        self.mem.inc_pc()
        self.inc_cycle()

    def clrw(self):
        self.W.set(0x00)
        self.zero_flag(self.W)
        self.mem.inc_pc()
        self.inc_cycle()

    def clrwdt(self):
        self.Watchdog_Timer = 0
        self.inc_cycle()
    
    def comf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(~self.mem[f])
            self.zero_flag(self.W)
        else:
            self.mem[f] = ~self.mem[f]
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()
        self.inc_cycle()

    def decfsz(self, f, d = 0):
        if d == 1:
            self.mem[f] = self.mem[f].decrement()
            if self.mem[f] & 0xFF == 0:
                self.mem.inc_pc()
                self.inc_cycle()
        else:
            self.W = W_Register(self.mem[f].decrement())
            if self.W & 0xFF == 0:
                self.mem.inc_pc()
                self.inc_cycle()
        self.mem.inc_pc()
        self.inc_cycle()

    def decf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(self.mem[f].decrement())
            self.zero_flag(self.W)
        else:
            self.mem[f] = self.mem[f].decrement()
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()
        self.inc_cycle()

    def goto(self, k):
        pclath43 = (self.mem[0xA].value & 0b11000) << 8
        self.mem.set_pc(k+pclath43)
        self.inc_cycle(2)
        return
    
    def incf(self, f, d = 0):
        if d == 0:
            self.W = W_Register(self.mem[f].increment())
            self.zero_flag(self.W)
        else:
            self.mem[f] = self.mem[f].increment()
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()
        self.inc_cycle()

    def incfsz(self, f, d = 0):
        if d == 1:
            self.mem[f] = self.mem[f].increment()
            if self.mem[f] & 0xFF == 0:
                print("is zero")
                self.mem.inc_pc()
                self.inc_cycle()
        else:
            self.W = W_Register(self.mem[f].increment())
            if self.W & 0xFF == 0:
                self.mem.inc_pc()
                self.inc_cycle()
        self.mem.inc_pc()
        self.inc_cycle()

    def iorlw(self, k):
        self.W |= k
        self.zero_flag(self.W)
        self.mem.inc_pc()
        self.inc_cycle()

    def iorwf(self, f, d  = 0):
        if d == 0:
            self.W |= self.mem[f]
            self.zero_flag(self.W)
        else:
            self.mem[f] |= self.W
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()
        self.inc_cycle()

    def movlw(self, k):
        self.W.set(k)
        self.mem.inc_pc()
        self.inc_cycle()

    def movf(self, f, d = 0):
        if d == 0:
            self.W.set(self.mem[f])
            self.zero_flag(self.W)
        else:
            self.mem[f].set(self.mem[f])
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()
        self.inc_cycle()
               
    def movwf(self, f):
        self.mem[f] = Register(self.W)
        self.mem.inc_pc()
        self.inc_cycle()
    
    def nop(self):
        self.mem.inc_pc()
        self.inc_cycle()
    
    def retfie(self):
        self.inc_cycle(2)
        self.mem[0xB].set_bit(7, 1)
        self.mem.set_pc(self.mem.pop_pc())
    
    def retlw(self, k):
        self.W.set(k)
        self.mem.set_pc(self.mem.pop_pc())
        self.inc_cycle(2)
        return
    
    def _return(self):
        self.mem.set_pc(self.mem.pop_pc())
        self.inc_cycle(2)
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
        self.inc_cycle()

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
        self.inc_cycle()

    def sleep(self):
        # Sleep Routine
        return
    
    def sublw(self, k):
        self.digit_carry_flag_sub(self.W, k)
        self.W = W_Register(k - self.W.value)
        self.carry_flag_sub(self.W)
        self.zero_flag(self.W)
        self.mem.inc_pc()
        self.inc_cycle()

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
        self.inc_cycle()

    def swapf(self, f, d = 0):
        higher = (self.mem[f].value & 0xF0) >> 4
        lower = self.mem[f].value & 0x0F
        self.mem[f] = Register((lower << 4) + higher)
        self.mem.inc_pc()
        self.inc_cycle()
    
    def xorlw(self, k):
        self.W ^= k
        self.zero_flag(self.W)
        self.mem.inc_pc()
        self.inc_cycle()

    def xorwf(self, f, d = 0):
        if d == 0:
            self.W ^= self.mem[f]
            self.zero_flag(self.W)
        else:
            self.mem[f] ^= self.W
            self.zero_flag(self.mem[f])
        self.mem.inc_pc()
        self.inc_cycle()
#endregion

#region flags
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
        if masked_k - masked_reg >= 0x0F:
            self.mem[STATUS].set_bit(DC, 1)
        else:
            self.mem[STATUS].set_bit(DC, 0)
         
#endregion
            
    def handle_Timer0(self, cycles):
        if cycles == -1:
            self.Vorteiler_count += 1
            if self.Vorteiler_count >= self.Vorteiler:
                self.mem.increment_timer0()
                self.Vorteiler_count %= self.Vorteiler
        if self.Timer0_changed > 0:
            self.Timer0_changed -= 1
            return
        if not self.mem.get_bank_specific_register(1, 1).test_bit(3):
            self.Vorteiler = pow(2, (self.mem.get_bank_specific_register(1, 1).value & 0x07) + 1)
        else:
            self.Vorteiler = 1
        if not self.mem.get_bank_specific_register(1, 1).test_bit(5):           
            self.Vorteiler_count += cycles
            if self.Vorteiler_count >= self.Vorteiler:
                self.mem.increment_timer0()
                self.Vorteiler_count %= self.Vorteiler
        if self.mem.get_bank_specific_register(1, 0).value > 0xFF:
            self.mem[1].set(0)
            self.mem[0xB].set_bit(2, 1)
    
    def handle_interrupts(self):
        intcon = self.mem[0xB]
        if intcon.test_bit(7):
            if (intcon.test_bit(5) and intcon.test_bit(2)) or (intcon.test_bit(4) and intcon.test_bit(1)) or (intcon.test_bit(3) and intcon.test_bit(0)):
                intcon.set_bit(7, 0)
                self.mem.push_pc()
                self.mem.set_pc(0x4)
                
    def handle_Watchdog(self, cycles):
        if self.Watchdog_enabled:
            self.Watchdog_Timer += (cycles/float(self.quartz))*4
            self.sig_Watchdog_Timer.emit(self.Watchdog_Timer)
            if self.mem.get_bank_specific_register(1, 1).test_bit(3):
                overflow = 18 * pow(2, self.mem.get_bank_specific_register(1, 1).value & 0x07)
            else:
                overflow = 18
            if self.Watchdog_Timer >= overflow:
                #Watchdog Timer Interrupt
                pass

    def set_interrupt_flags(self, old_rb:Register):
        intcon = self.mem[0xB]
        option = self.mem.get_bank_specific_register(1, 1)
        if option.test_bit(6) and not old_rb.test_bit(0) and self.mem[6].test_bit(0):
            intcon.set_bit(1, 1)
        elif not option.test_bit(6) and old_rb.test_bit(0) and not self.mem[6].test_bit(0):
            intcon.set_bit(1, 1)
        
        changed_bit = (old_rb.value & 0b11110000) ^ (self.mem[6].value & 0b11110000)
        index = 0
        while changed_bit > 1:
            index += 1
            changed_bit = changed_bit >> 1
        
        if self.mem.get_bank_specific_register(6, 1).test_bit(index) and changed_bit:
            intcon.set_bit(0, 1)
          
    def inc_cycle(self, amount = 1):
        self.cycle += amount
        self.handle_Watchdog(amount)
        self.sig_runtime.emit(self.cycle)
        self.handle_Timer0(amount)
        
#region signals
                    
    def update_mem(self):
        self.sig_mem.emit((self.mem, self.W))
        
    def update_quartz(self):
        self.sig_quartz.emit(self.quartz)
        
    def update_inst(self, inst):
        self.sig_inst.emit(self.inst)
    
    def update_pc(self):
        self.sig_pc.emit(self.mem.pc)
        
    def update_pc(self):
        self.sig_pc.emit(self.mem.pc)    
            
    @pyqtSlot(bool)
    def handle_Timer0_changed(self, signal):
        self.Timer0_changed = 2
        self.Vorteiler_count = 0
            
    @pyqtSlot(bool)
    def handle_pclath(self):
        if not self.inst_pcl_set:
            self.mem.set_pc(self.mem[2].value + (self.mem[0xA].value << 8))
    
    @pyqtSlot(bool)
    def run_instructions(self, signal):
        if signal:
            self.step()
            # time.sleep(0.1)
            self.sig_continue.emit(True)
            
        
    @pyqtSlot(bool)
    def step(self):
        debugpy.debug_this_thread()
        self.tmp_rb = self.mem[6]
        self.execute_instruction()
        self.set_interrupt_flags(self.tmp_rb)
        self.handle_interrupts()
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
        if update[0] == 6:
            tmp_rb = Register(0 if update[2] else 1)
        self.mem[update[0]].set_bit(update[1], update[2])
        if update == [5, 4, 1] and self.mem.get_bank_specific_register(1, 1).test_bit(5) and not self.mem.get_bank_specific_register(1, 1).test_bit(4):
            self.handle_Timer0(-1)
        if update == [5, 4, 0] and self.mem.get_bank_specific_register(1, 1).test_bit(5) and self.mem.get_bank_specific_register(1, 1).test_bit(4):
            self.handle_Timer0(-1)
        if update[0] == 6:
            self.set_interrupt_flags(tmp_rb)
        self.update_mem()
        
    @pyqtSlot(list)
    def update_table_input_mem(self, item:list):
        self.mem[item[0]] = item[1]
        self.update_mem()
    
    @pyqtSlot(bool)
    def set_startup_variables(self):
        self.mem.reset()
        self.update_mem()
        
    @pyqtSlot(float)
    def set_freq(self, value):
        self.quartz = value
        
    @pyqtSlot(bool)
    def set_wd_enabled(self, value):
        self.Watchdog_enabled = value

#endregion
           
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
        self.inst_pcl_set = True
        self.mem[2] = (self.mem.pc & 0b0000011111111)
        self.inst_pcl_set = False                
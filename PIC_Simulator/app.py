# from lst_parser_fuer_text import Listing as Listing_txt
from lst_parser_bits import Listing
from control.processor import Processor
from view.basewindow import BaseWindow

#from random import randint

class Application():
    lst = Listing(filePath="C:\\Users\\xcx1833\\OneDrive - Atruvia\\Dokumente\\DHBW\\Rechnertechnik_2\\git\\PIC-16F84-Simulator\\PIC-16F84-Simulator\\ExamplesListings\\TPicSim8.LST")
    lst.create_instructions()
    inst = lst.get_instructions()
    p = Processor(inst)
    gui = BaseWindow(tableData = p.mem.eeprom)

    def __init__(self):
        self.lst = Listing(filePath="C:\\Users\\xcx1833\\OneDrive - Atruvia\\Dokumente\\DHBW\\Rechnertechnik_2\\git\\PIC-16F84-Simulator\\PIC-16F84-Simulator\\ExamplesListings\\TPicSim8.LST")
        self.lst.create_instructions()
        self.inst = self.lst.get_instructions()
        p = Processor(self.inst)
        gui = BaseWindow(tableData = self.p.mem.eeprom)
    p.movlw(10)
    p.movwf(1)
    gui.setMemData(p.mem.eeprom)
    gui.init_window()

    def update_mem_gui(self):
        self.gui.tableData = self.p.mem.eeprom


#region tests
# p.addlw(randint(0,255))
# p.andlw(randint(0,255))
# p.addwf(randint(0x10, 0x4F), 0)
# p.andwf(randint(0x10, 0x4F), 1)
# p.bcf('W', 1)
# p.btfsc('W', 1)
# p.bsf('W', 1)
# p.btfss('W', 1)
# p.clrf(randint(0x10, 0x4F))
# p.clrw()
# p.comf(randint(0x10, 0x4F), 0)
# p.decfsz(randint(0x10, 0x4F), 0)
# p.decf(randint(0x10, 0x4F), 0)
# p.incf(randint(0x10, 0x4F), 0)
# p.incfsz(randint(0x10, 0x4F), 0)
# p.iorlw(randint(0,255))
# p.iorwf(randint(0x10, 0x4F), 0)
# p.movlw(randint(0,255))
# p.movf(randint(0x10, 0x4F), 0)
# p.movwf(randint(0x10, 0x4F))
# p.nop()
# p.retfie()
# p.retlw(randint(0,255))
# p._return()
# print("return")
# p.rlf(randint(0x10, 0x4F), 0)
# p.rrf(randint(0x10, 0x4F), 0)
# p.sublw(randint(0,255))
# p.subwf(randint(0x10, 0x4F), 0)
# p.xorlw(randint(0,255))
# p.xorwf(randint(0x10, 0x4F), 0)

# print(p.W)
# print(p.mem)

# print(p.mem.pc)
# print(p.mem.stack)
# p.goto(5)
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p.call(randint(0,255))
# print("call")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)
# p._return()
# print("return")
# print(p.mem.pc)
# print(p.mem.stack)

# print(inst)
#endregion
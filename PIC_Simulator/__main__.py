from lst_parser_bits import Listing
from control.processor import Processor
from view.basewindow import BaseWindow

lst = Listing(filePath="C:\\Users\\Dsche\\OneDrive\\Documents\\Studium\\Rechnertechnik\\Projekt\\PIC-16F84-Simulator\\ExamplesListings\\TPicSim1.LST")
lst.create_instructions()
inst = lst.get_instructions()
p = Processor(inst)
gui = BaseWindow(tableData = p.mem.eeprom)

def __init__(self):
    self.lst = Listing(filePath="C:\\Users\\Dsche\\OneDrive\\Documents\\Studium\\Rechnertechnik\\Projekt\\PIC-16F84-Simulator\\ExamplesListings\\TPicSim1.LST")
    self.lst.create_instructions()
    self.inst = self.lst.get_instructions()
    p = Processor(self.inst)
    gui = BaseWindow(tableData = self.p.mem.eeprom)
    
p.movlw(10)
p.movwf(1)
gui.setMemData(p.mem.eeprom)
gui.init_window()

from lst_parser_bits import Listing
from control.processor import Processor
from view.basewindow import BaseWindow

lst = Listing(filePath="./ExamplesListings/TPicSim1.LST")
lst.create_instructions()
inst = lst.get_instructions()
p = Processor(inst)
gui = BaseWindow(tableData = p.mem.eeprom)
    
p.movlw(10)
p.movwf(1)
gui.setMemData(p.mem.eeprom)
gui.init_window()

from model.memory import Memory
from parser import Listing
from control.processor import Processor

p = Processor(lst = Listing(filePath="C:\\Users\\xcx1833\\OneDrive - Atruvia\\Dokumente\\DHBW\\Rechnertechnik_2\\git\\PIC-16F84-Simulator\\PIC-16F84-Simulator\\PIC_Simulator\\ExampleListings\\TPicSim8.LST"))

print(p.W.value)
p.addlw(10)
print(p.W)
p.andwf(1,1)
for reg in p.mem.eeprom:
    print(reg)
from lst_parser_fuer_text import Listing as Listing_txt
from lst_parser_bits import Listing
from control.processor import Processor

from random import randint

lst = Listing(filePath="C:\\Users\\xcx1833\\OneDrive - Atruvia\\Dokumente\\DHBW\\Rechnertechnik_2\\git\\PIC-16F84-Simulator\\PIC-16F84-Simulator\\PIC_Simulator\\ExampleListings\\TPicSim101.LST")

lst.create_instructions()

# inst = lst.get_instructions()
# JPs = lst.get_JPs()

# p = Processor(inst, JPs)

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
# p.rlf(randint(0x10, 0x4F), 0)
# p.rrf(randint(0x10, 0x4F), 0)
# p.sublw(randint(0,255))
# p.subwf(randint(0x10, 0x4F), 0)
# p.xorlw(randint(0,255))
# p.xorwf(randint(0x10, 0x4F), 0)

# print(p.W)
# print(p.mem)
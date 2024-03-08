from model.memory import Memory
from model.registers import Register
from parser import Listing

class Processor():

    mem = Memory
    W = Register
    quartz = int
    lst = Listing

    def __init__(self, lst) -> None:
        self.lst = lst
        lst.create_instructions()
        print(lst.instructions)
        self.W.value = 0

    def addlw(self, k):
        self.W = self.W + k


    def andlw(self, k):
        self.W = self.W & k

    def addwf(self, f, d = 0):
        if d == 0:
            self.W = self.W + self.mem.eeprom[f]
        else:
            self.mem.eeprom[f] = self.mem.eeprom[f] +self.W

    def andwf(self, f, d = 0):
        if d == 0:
            self.W = self.W & self.mem.eeprom[f].value
        else:
            self.mem.eeprom[f] = self.mem.eeprom[f] & self.W
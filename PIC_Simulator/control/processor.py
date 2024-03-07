from model.memory import Memory
from model.registers import Register
from parser import Listing

class Processor():

    mem = Memory
    W = Register(0x00)
    quartz = int
    lst = Listing

    def __init__(self, lst) -> None:
        self.lst = lst
        lst.create_instructions()
        print(lst.instructions)

    def addlw(self, k):
        self.W += k

    def andlw(self, k):
        self.W = self.W & k

    def addwf(self, f, d = 0):
        if d == 0:
            self.W += f.value
        else:
            f += self.W.value

    def andwf(self, f, d = 0):
        if d == 0:
            self.W &= f.value
        else:
            f &= self.W.value
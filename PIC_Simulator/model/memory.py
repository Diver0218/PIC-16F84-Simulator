from .registers import Register

class Memory():

    # Bank 0
    # INDF : Register
    # TMR0 : Register
    # PCL : Register
    # STATUS : Register
    # FSR : Register
    # PORTA : Register
    # PORTB : Register
    # EEDATA : Register
    # EEADR : Register
    # PCLATH : Register
    # INTCON : Register

    # # Bank 1
    # OPTION_REG : Register
    # TRISA : Register
    # TRISB : Register
    # EECON1 : Register
    # EECON2 : Register

    eeprom = [[Register(0)] *2 ] * 80

    stackpointer : int = 0

    stack : list[int] = [int(0)] * 8

    pc : int = 0

    def __str__(self):
        retValue = ""
        index = 0
        for reg in self.eeprom:
            retValue += f"Adresse: {index:02X}, Bank 0: {str(reg[0])}, Bank 1: {str(reg[1])}'\n'"
            index += 1
        return retValue
    
    def __setitem__(self, index, value):
        
        self.eeprom[index] = value

    def __getitem__(self, index):
        return self.eeprom[index]
    
    def inc_pc(self, amount : int = 1):
        self.pc += amount

    def set_pc(self, pc):
        self.pc = pc

    def push_pc(self):
        if self.stackpointer >= 7:
            self.stackpointer = 0
        else:
            self.stackpointer += 1
        self.stack[self.stackpointer] = self.pc


    def pop_pc(self):
        retAdr = self.stack[self.stackpointer]
        if self.stackpointer <= 0:
            self.stackpointer = 7
        else:
            self.stackpointer -= 1
        return retAdr
    
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

    eeprom = [Register(0)] * 80

    stackpointer : int = 0

    stack = []

    pc : int = 0

    def __str__(self):
        retValue = ""
        index = 0
        for reg in self.eeprom:
            retValue += f"Adresse: {index:02X}, " + str(reg) + '\n'
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
        self.stack.append(self.pc)
        if len(self.stack) > 8:
            self.stack.pop(0)

    def pop_pc(self):
        if len(self.stack) == 0:
            return None
        return self.stack.pop()
    
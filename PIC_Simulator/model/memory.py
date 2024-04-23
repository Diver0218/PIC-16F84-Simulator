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

    eeprom = [[Register(0) for _ in range(80)] for _ in range(2)]

    stackpointer : int = 0

    stack : list[int] = [int(0)] * 8

    pc : int = 0
    
    bank_relevant_adr = [0x01, 0x05, 0x06, 0x08, 0x09]

    def __str__(self):
        retValue = ""
        bank0 = self.eeprom[0]
        bank1 = self.eeprom[1]
        for index in range(len(bank0)):
            retValue += f"Adresse: {index:02X}, Bank 0: {str(bank0[index])}, Bank 1: {str(bank1[index])}'\n'"
        return retValue
    
    def __setitem__(self, index, value):
        if self.eeprom[0][3].test_bit(5) and index in self.bank_relevant_adr:
            self.eeprom[1][index] = value
        else:
            self.eeprom[0][index] = value

    def __getitem__(self, index):
        if self.eeprom[0][3].test_bit(5) and index in self.bank_relevant_adr:
            return self.eeprom[1][index]    
        else:
            return self.eeprom[0][index] 

    def get_bank_specific_register(self, index, bank):
        if bank and index in self.bank_relevant_adr:
            return self.eeprom[1][index]    
        else:
            return self.eeprom[0][index]
                    
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
    
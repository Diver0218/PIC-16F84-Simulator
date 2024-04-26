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

    def __init__(self):
        self.eeprom = [[Register(0) for _ in range(80)] for _ in range(2)]
        self.stackpointer : int = 0
        self.stack : list[int] = [int(0) for _ in range(8)] 
        self.pc : int = 0   
        self.bank_relevant_adr = [0x01, 0x05, 0x06, 0x08, 0x09]

    def __str__(self):
        retValue = ""
        bank0 = self.eeprom[0]
        bank1 = self.eeprom[1]
        for index in range(len(bank0)):
            retValue += f"Adresse: {index:02X}, Bank 0: {str(bank0[index])}, Bank 1: {str(bank1[index])}'\n'"
        return retValue
    
    def __setitem__(self, index, value):
        tuple_index = self._handle_index(index)
        if (self.eeprom[0][3].test_bit(5) and index in self.bank_relevant_adr) or tuple_index[1]:
            self.eeprom[1][tuple_index[0]] = value
        else:
            self.eeprom[0][tuple_index[0]] = value

    def __getitem__(self, index):
        tuple_index = self._handle_index(index)
        if (self.eeprom[0][3].test_bit(5) and index in self.bank_relevant_adr) or tuple_index[1]:
            return self.eeprom[1][tuple_index[0]]    
        else:
            return self.eeprom[0][tuple_index[0]] 

    def get_bank_specific_register(self, index, bank):
        if bank and index in self.bank_relevant_adr:
            return self.eeprom[1][index]    
        else:
            return self.eeprom[0][index]
    
    def _handle_index(self, index):
        if index < 80:
            return [index, 0]
        elif index < 128:
            return [-1, 0]
        elif index < 208:
            if index - 128 in self.bank_relevant_adr:
                return [index - 128, 1]
            else:
                return [index - 128, 0]
                    
    def inc_pc(self, amount : int = 1):
        self.pc += amount

    def set_pc(self, pc):
        self.pc = pc

    def push_pc(self):
        if self.stackpointer >= 7:
            self.stack[self.stackpointer] = self.pc + 1
            self.stackpointer = 0
        else:
            self.stack[self.stackpointer] = self.pc + 1
            self.stackpointer += 1

    def pop_pc(self):
        if self.stackpointer <= 0:
            self.stackpointer = 7
            retAdr = self.stack[self.stackpointer]
        else:
            self.stackpointer -= 1
            retAdr = self.stack[self.stackpointer]
        return retAdr
    
    def reset(self):
        for item in self.eeprom[0]:
            item.set(0)
        for item in self.bank_relevant_adr:
            self.eeprom[1][item].set(0)
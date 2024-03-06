class Register():

    value : int

    def __init__(self):
        self.set(0x00)

    def set(self, value : int):
        if value > 0xFF:
            self.set(value - 0xFF)
            # set overload flagg
        else:
            self.value = value
    
    def increment(self):
        self.value += 1
        if self.value > 0xFF:
            self.value = 0x00
            # set overload flagg

    def decrement(self):
        self.value -= 1
        if self.value < 0x00:
            self.value = 0xFF
            # set overload flagg

class Memory():

    # Bank 0
    INDF : Register
    TMR0 : Register
    PCL : Register
    STATUS : Register
    FSR : Register
    PORTA : Register
    PORTB : Register
    EEDATA : Register
    EEADR : Register
    PCLATH : Register
    INTCON : Register

    # Bank 1
    OPTION_REG : Register
    TRISA : Register
    TRISB : Register
    EECON1 : Register
    EECON2 : Register

    W : Register = 0x00

    eeprom : Register = [0] * 68

    stackpointer : int

    stack : int


mem = Memory()

print(mem.eeprom)


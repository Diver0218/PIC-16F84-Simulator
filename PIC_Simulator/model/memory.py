from .registers import Register

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

    stack : int = [0] * 68



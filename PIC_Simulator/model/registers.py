from PyQt6.QtCore import QObject, pyqtSignal
class Register(QObject):

    value : int
    sig_data_latch = pyqtSignal(object)

    def __init__(self, value=0x00, parent = None):
        super().__init__()
        self.parent = parent
        if parent:
            self.sig_data_latch.connect(parent.set_data_latch)
        self.set(value)

    def set(self, value):
        if isinstance(value, int):
            self.value = value
        elif isinstance(value, Register):
            self.value = value.value
        else:
            raise TypeError("Unsupported Type for 'set' method")
        if self.parent:
            self.sig_data_latch.emit(self)
    
    def increment(self):
        retval = self.value + 1
        retval &= 0xFF
        return Register(retval)

    def decrement(self):
        retval = self.value - 1
        if retval < 0:
            retval = 0xFF
        return Register(retval)
    
    def __str__(self):
        return f"{self.value:02X}"

    def __and__(self, other):
        if isinstance(other, Register):  
            retValue = self.value & other.value
        elif isinstance(other, int):
            retValue = self.value & other
        else:
            raise TypeError("Unsupported operand type(s) for &: 'Register' and '{}'".format(type(other)))
        # set zeroflag
        return Register(retValue)
            
    def __iand__(self, other):
        if isinstance(other, Register):  
            self.value &= other.value
        elif isinstance(other, int):
            self.value &= other
        else:
            raise TypeError("Unsupported operand type(s) for &=: 'Register' and '{}'".format(type(other)))
        # set zeroflag
        return self
    
    def __or__(self, other):
        if isinstance(other, Register):  
            retValue = self.value | other.value
        elif isinstance(other, int):
            retValue = self.value | other
        else:
            raise TypeError("Unsupported operand type(s) for &: 'Register' and '{}'".format(type(other)))
        # set zeroflag
        return Register(retValue)

    def __ior__(self, other):
        if isinstance(other, Register):  
            self.value |= other.value
        elif isinstance(other, int):
            self.value |= other
        else:
            raise TypeError("Unsupported operand type(s) for &=: 'Register' and '{}'".format(type(other)))
        # set zeroflag
        return self

    def set_bit(self, index, value):
        mask = 1 << index
        self &= ~mask
        if value:
            self |= mask
        if self.parent:
            self.sig_data_latch.emit(self)

    def test_bit(self, index):
        return (self & (1 << index)).value >> index
    
    def __lshift__(self, other):
        return Register(self.value << other)
    
    def __rshift__(self, other):
        return Register(self.value >> other)
    
    def __ilshift__(self, other):
        self = self << other
        return self
    
    def __irshift__(self, other):
        self = self >> other
        return self
    
    def __xor__(self, other):
        if isinstance(other, Register):  
            retValue = self.value ^ other.value
        elif isinstance(other, int):
            retValue = self.value ^ other
        else:
            raise TypeError("Unsupported operand type(s) for &: 'Register' and '{}'".format(type(other)))
        # set zeroflag
        return Register(retValue)

    def __ixor__(self, other):
        if isinstance(other, Register):  
            self.value ^= other.value
        elif isinstance(other, int):
            self.value ^= other
        else:
            raise TypeError("Unsupported operand type(s) for &=: 'Register' and '{}'".format(type(other)))
        # set zeroflag
        return self
    
    def __invert__(self):
        return Register((~self.value) & 0xFF)
    
    def __neg__(self):
        return Register(-self.value)
    
    def __mod__(self, other):
        if isinstance(other, Register):
            retValue = self.value % other.value
        elif isinstance(other, int):
            retValue = self.value % other
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Register' and '{}'".format(type(other)))
        return Register(retValue)
    
    def __iadd__(self, other):
        if isinstance(other, Register):
            self.value += other.value
        elif isinstance(other, int):
            self.value += other
        else:
            raise TypeError("Unsupported operand type(s) for +=: 'Register' and '{}'".format(type(other)))
        return self
    
    def __sub__(self, other):
        if isinstance(other, Register):
            retValue = self.value - other.value
        elif isinstance(other, int):
            retValue = self.value - other
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Register' and '{}'".format(type(other)))
        return W_Register(retValue)
    
    def __eq__(self, other):
        if isinstance(other, Register):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        else:
            raise TypeError("Unsupported operand type(s) for ==: 'Register' and '{}'".format(type(other)))
    
class W_Register(Register):

    def __init__(self, value, parent = None):
        self.parent = parent
        if isinstance(value, Register):
            self.set(value.value)
        elif isinstance(value, int):
            self.set(value)
        

    def __add__(self, other):
        if isinstance(other, Register):
            retValue = self.value + other.value
            # overload flag
        elif isinstance(other, int):
            retValue = self.value + other
            # overload flag
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Register' and '{}'".format(type(other)))
        return W_Register(retValue)
                
    def __isub__(self, other):
        if isinstance(other, Register):
            self.value -= other.value
            # overload flag
        elif isinstance(other, int):
            self.value -= other
            # overload flag
        else:
            raise TypeError("Unsupported operand type(s) for +=: 'Register' and '{}'".format(type(other)))
        return self
    
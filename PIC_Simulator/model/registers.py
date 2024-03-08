class Register():

    value : int

    def __init__(self, value=0x00):
        self.set(value)

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
            # set overload flag
    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        if type(other) == Register:          
            retValue = self.value + other.value
        elif type(other) == int:
            retValue = self.value = other
        # if self.value > 0xFF:
        #     self.value = 0x00
        #     # set overload flagg
        return retValue
        # zeroflag
            
    def __iadd__(self, other):
        return self + other

    def __and__(self, other):
        if type(other) == Register:  
            retValue = self.value & other.value
        elif type(other) == int:
            retValue = self.value & other
        # set zeroflag
            return retValue
            
    def __iand__(self, other):
        return self & other

    
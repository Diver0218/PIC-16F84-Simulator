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
            # set overload flagg

    def __add__(self, other):
        self.value += other
        if self.value > 0xFF:
            self.value = 0x00
            # set overload flagg
        # zeroflag

    def __and__(self, other):
        self.value = self.value & other
        # set zeroflag

    
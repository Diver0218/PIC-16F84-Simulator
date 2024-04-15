import os

class Listing():

    def __init__(self) -> None:
        pic_sim_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(pic_sim_dir)
        self.filePath = os.path.join(project_root, "ExamplesListings", "TPicSim1.LST")

    filePath : str

    instructions = []

    def create_instructions(self):
        self.readFile()
        # print(self)

    def readFile(self):
        pc_index = 0
        with open(self.filePath, 'r') as file:
            for line in file:
                self.parseLine(line)

    def parseLine(self, line):
        if line[0] == ' ':
            return
        else:
            self.instructions.append({
                'pc' : int(line[0:4], 16),
                'inst' : self.extract_instruction(int(line[5:9], 16)),
            })

    def __str__(self):
        retValue = ''
        for line in self.instructions:
            retValue += str(line) + '\n'
        return retValue
    
    def extract_instruction(self, opcode):

        if (opcode & 0b1111_1111_0000_0000) == 0b0000_0111_0000_0000:
            return {
                'inst': 'addwf',
                'destination': (opcode & 0b00_00_0000_1000_0000) >> 7,
                'file': opcode & 0b00_00_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_0101_0000_0000:
            return {
                'inst': 'andwf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0x0b1111_1111_1000_0000) == 0b0000_0001_1000_0000:
            return {
                'inst': 'clrf',
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_1000_0000) == 0b0000_0001_0000_0000:
            return {
                'inst': 'clrw',
            }
        
        if (opcode & 0b1111_1111_1000_0000) == 0b0000_0001_0000_0000:
            return {
                'inst': 'clrw',
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_1001_0000_0000:
            return {
                'inst': 'comf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_0011_0000_0000:
            return {
                'inst': 'decf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_1011_0000_0000:
            return {
                'inst': 'decfsz',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_1010_0000_0000:
            return {
                'inst': 'incf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_1111_0000_0000:
            return {
                'inst': 'incfsz',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_0100_0000_0000:
            return {
                'inst': 'iorwf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_1000_0000_0000:
            return {
                'inst': 'movf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_1000_0000) == 0b0000_0000_1000_0000:
            return {
                'inst': 'movwf',
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_1001_1111) == 0b0000_0000_0000_0000:
            return {
                'inst': 'nop',
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_1101_0000_0000:
            return {
                'inst': 'rlf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_1100_0000_0000:
            return {
                'inst': 'rrf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_0010_0000_0000:
            return {
                'inst': 'subwf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_1110_0000_0000:
            return {
                'inst': 'swapf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0000_0110_0000_0000:
            return {
                'inst': 'xorwf',
                'destination': (opcode & 0b0000_0000_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1100_0000_0000) == 0b0001_0000_0000_0000:
            return {
                'inst': 'bcf',
                'bit': (opcode & 0b0000_0011_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1100_0000_0000) == 0b0001_0100_0000_0000:
            return {
                'inst': 'bsf',
                'bit': (opcode & 0b0000_0011_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1100_0000_0000) == 0b0001_1000_0000_0000:
            return {
                'inst': 'btfsc',
                'bit': (opcode & 0b0000_0011_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1100_0000_0000) == 0b0001_1100_0000_0000:
            return {
                'inst': 'btfss',
                'bit': (opcode & 0b0000_0011_1000_0000) >> 7,
                'file': opcode & 0b0000_0000_0111_1111,
            }
        
        if (opcode & 0b1111_1110_0000_0000) == 0b0011_1110_0000_0000:
            return {
                'inst': 'addlw',
                'literal': opcode & 0b0000_0000_1111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0011_1001_0000_0000:
            return {
                'inst': 'andlw',
                'literal': opcode & 0b0000_0000_1111_1111,
            }
        
        if (opcode & 0b1111_1000_0000_0000) == 0b0010_0000_0000_0000:
            return {
                'inst': 'call',
                'literal': opcode & 0b0000_0111_1111_1111,
            }
        
        if opcode == 0b0000_0000_0110_0100:
            return {
                'inst': 'clrwdt',
            }
        
        if (opcode & 0b1111_1000_0000_0000) == 0b0010_1000_0000_0000:
            return {
                'inst': 'goto',
                'literal': opcode & 0b0000_0111_1111_1111,
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0011_1000_0000_0000:
            return {
                'inst': 'iorlw',
                'literal': opcode & 0b0000_0000_1111_1111,
            }
        
        if (opcode & 0b1111_1100_0000_0000) == 0b0011_0000_0000_0000:
            return {
                'inst': 'movlw',
                'literal': opcode & 0b0000_0000_1111_1111,
            }
        
        if opcode == 0b0000_0000_0000_1001:
            return {
                'inst': 'retfie',
            }     

        if (opcode & 0b1111_1100_0000_0000) == 0b0011_0100_0000_0000:
            return {
                'inst': 'retlw',
                'literal': opcode & 0b0000_0000_1111_1111,
            }
        
        if (opcode & 0b1111_1100_0000_0000) == 0b0011_0100_0000_0000:
            return {
                'inst': 'retlw',
                'literal': opcode & 0b0000_0000_1111_1111,
            }
        
        if opcode == 0b0000_0000_0000_1000:
            return {
                'inst': 'return',
            }
          
        if opcode == 0b0000_0000_0110_0011:
            return {
                'inst': 'sleep',
            }
        
        if (opcode & 0b1111_1111_0000_0000) == 0b0011_1010_0000_0000:
            return {
                'inst': 'sublw',
                'literal': opcode & 0b0000_0000_1111_1111,
            }
    def get_instructions(self):
        return self.instructions
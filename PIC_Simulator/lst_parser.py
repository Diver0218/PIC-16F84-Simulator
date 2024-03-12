import re

class Listing():

    def __init__(self, filePath) -> None:
        self.filePath = filePath

    filePath : str

    instructions = []
    names = []
    JPs = []

    def create_instructions(self):
        self.readFile()
        # print(self.instructions)
        # print(self.names)
        self.replace_names()
        # print(self.instructions)
        self.format_nmbr()
        print(self.instructions)
        print(self.JPs)

    def readFile(self):
        pc_index = 0
        with open(self.filePath, "r") as file:
            for line in file:
                inst_len = len(self.instructions)
                self.parseLine(line, pc_index)
                if len(self.instructions) > inst_len:
                    pc_index += 1


    def parseLine(self, line : str, pc_index : int):

        # Anfang abschneiden
        line = line[27:]

        # Kommentare entfernen
        line = line.split(";")[0]

        # Zwischen instruction und Jumppoint unterscheiden
        if line[0] != " " and not line.isspace():
            self.JPs.append({
                'jmp_name': line.strip(),
                'pc_index': pc_index + 1,
            })
            return
        else:
            line = line.strip()
            if line == '':
                return
            if "equ" in line:
                self.names.append(self.safe_name(line))
                return
            self.instructions.append(self.extract_cmd(line))
            return
    
    def extract_cmd(self, cmd):

        parts = cmd.split(" ")
        inst = parts[0]

        if len(parts) == 2:
            args = parts[1].split(",")
            arg1 = args[0]
            if len(args) == 2:
                arg2 = args[1]
                return {
                    'inst': inst,
                    'arg1': arg1,
                    'arg2' : arg2,
                }
            else:
                return {
                    'inst': inst,
                    'arg1': arg1,
                }
        elif len(parts) == 1:
            return {
                'inst': parts[0]
            }
        else:
            raise Exception("Unknown Instruction in Listing")
            
    def safe_name(self, line):
        parts = line.split(" ")
        name = parts[0]
        adress = parts[-1]
        return {
            'name': name,
            'adr': adress,
        }
    

    def replace_names(self):
        for one_inst in self.instructions:
            if 'arg1' in one_inst.keys():
                for name in self.names:
                    if one_inst['arg1'] == name['name']:
                        one_inst['arg1'] = name['adr']


    def format_nmbr(self):
        for inst in self.instructions:
            if 'arg1' in inst.keys():
                if re.match(".*[Bb]$", str(inst['arg1'])):
                    inst['arg1'] = int(inst['arg1'][:len(inst['arg1'] ) - 1], 2)
                    # print("bin: "+ str(inst['arg1']))
                if re.match(".*[Hh]$", str(inst['arg1'])):
                    inst['arg1'] = int(inst['arg1'][:len(inst['arg1'] ) - 1], 16)
                    # print("hex: " + str(inst['arg1']))

    def get_instructions(self):
        return self.instructions
    
    def get_JPs(self):
        return self.JPs
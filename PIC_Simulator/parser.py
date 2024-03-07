

class Listing():

    def __init__(self, filePath) -> None:
        self.filePath = filePath

    filePath : str

    instructions = []
    names = []

    def create_instructions(self):
        self.readFile()
        print(self.instructions)
        print(self.names)
        self.replace_names()
        print(self.instructions)

    def readFile(self):
        with open(self.filePath, "r") as file:
            for line in file:
                self.parseLine(line)


    def parseLine(self, line : str):

        # Anfang abschneiden
        line = line[27:]

        # Kommentare entfernen
        line = line.split(";")[0]

        # Zwischen instruction und Jumppoint unterscheiden
        if line[0] != " " and not line.isspace():
            self.instructions.append({
                'inst': "JP",
                'jmp_name': line.strip()
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
            
    def safe_name(self, line):
        parts = line.split(" ")
        name = parts[0]
        adress = parts[2]
        return {
            'name': name,
            'adr': adress,
        }
    

    def replace_names(self):
        for inst in self.instructions:
            for name in self.names:
                if inst.arg1 == name.name:
                    inst.arg1 = name.adr


    # def format_adr(self):
    #     for inst in self.instructions:
    #         #asd

        
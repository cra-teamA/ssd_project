import json

ERROR = 'ERROR'
SSD_NAND_PATH = 'ssd_nand.txt'
SSD_OUTPUT_PATH = 'ssd_output.txt'
class SSDController:
    def __init__(self):
        ...
    def read(self,addr:int):
        if addr < 0 or addr > 99:
            self.output(ERROR)
            return
        with open(SSD_NAND_PATH, "r", encoding="utf-8") as f:
            data = json.load(f).get(str(addr))
        self.output(data)

    def output(self, data):
        with open(SSD_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(data)

    def write(self,addr, value):
        pass
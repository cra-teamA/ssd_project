import json
SSD_NAND_PATH = 'ssd_nand.txt'
SSD_OUT_PATH = 'ssd_output.txt'
class SSDController:
    def __init__(self):
        ...
    def read(self,addr:int):

        with open(SSD_NAND_PATH, "r", encoding="utf-8") as f:
            data = json.load(f).get(str(addr))
        print(data)
        with open(SSD_OUT_PATH, "w", encoding="utf-8") as f:
            f.write(data)

    def write(self,addr, value):
        pass
import random

from scripts.BaseScript import BaseScript
from shell.shell import Shell

class FullWriteReadCompare(BaseScript):
    def __init__(self, shell_interface:Shell):
        self.shell = shell_interface


    def run(self):


        for group in range(20):
            value = f"0x{random.getrandbits(32):08x}"

            start_lba = group * 5
            end_lba = start_lba + 5

            for lba in range(start_lba, end_lba):
                self.shell.write(f"W {lba} {value}")

            for lba in range(start_lba, end_lba):
                result = self.shell.read(f"R {lba} {value}")



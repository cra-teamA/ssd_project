from .BaseScript import BaseScript
import random

class PartialLBAWrite(BaseScript):
    def __init__(self, shell_interface):
        super().__init__(shell_interface)

    def run(self):
        lbas = [4, 0, 3, 1, 2]
        LOOP_COUNT = 30

        for data in range(LOOP_COUNT):
            for lba in lbas:
                self.write_lba(lba, data)

            for lba in lbas:
                if self.read_lba(lba) != data:
                    return False
        return True

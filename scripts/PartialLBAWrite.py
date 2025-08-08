from .BaseScript import BaseScript
import random

class PartialLBAWrite(BaseScript):
    def run(self):
        lbas = [4, 0, 3, 1, 2]
        LOOP_COUNT = 30

        for value in range(LOOP_COUNT):
            data = f"0x{value:08x}"
            for lba in lbas:
                self.write_lba(lba, data)

            for lba in lbas:
                if self.read_lba(lba) != data:
                    return False
        return True

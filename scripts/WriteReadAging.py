from .BaseScript import BaseScript
import random

class WriteReadAging(BaseScript):
    def __init__(self, shell_interface):
        super().__init__(shell_interface)

    def run(self):
        LOOP_COUNT = 100

        for _ in range(LOOP_COUNT):
            data1 = random.randint(1, 0x7fffffff)
            data2 = random.randint(1, 0x7fffffff)

            self.write_lba(0, data1)
            self.write_lba(99, data2)

            if data1 != self.read_lba(0) or data2 != self.read_lba(99):
                return False
        return True
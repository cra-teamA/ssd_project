from .BaseScript import BaseScript
import random
class WriteReadAging(BaseScript):
    def run(self):
        LOOP_COUNT = 100

        for _ in range(LOOP_COUNT):
            value1 = random.randint(1, 0x7fffffff)
            value2 = random.randint(1, 0x7fffffff)
            data1 = f"0x{value1:08x}"
            data2 = f"0x{value2:08x}"

            self.write_lba(0, data1)
            self.write_lba(99, data2)

            if data1 != self.read_lba(0) or data2 != self.read_lba(99):
                return False
        return True
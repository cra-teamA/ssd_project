from scripts.BaseScript import BaseScript
from shell.shell import Shell

class FullWriteReadCompare(BaseScript):
    def __init__(self, shell_interface:Shell):
        self.shell = shell_interface


    def run(self):
        lba_total = 100
        group_size = 5
        group_count = lba_total // group_size
        try:
            for group in range(group_count):
                value = f"0x{group:08x}"

                start_lba = group * group_size
                end_lba = start_lba + group_size

                for lba in range(start_lba, end_lba):
                    self.shell.write(f"W {lba} {value}")

                for lba in range(start_lba, end_lba):
                    result = self.shell.read(f"R {lba}")
                    if result != value:
                        return False

            return True
        except Exception as e:
            print(f"Exception during write/read: {e}")
            return False

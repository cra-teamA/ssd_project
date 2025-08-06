from .BaseScript import BaseScript

class FullWriteReadCompare(BaseScript):
    def __init__(self, shell_interface):
        super().__init__(shell_interface)


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
                    self.write_lba(lba, value)

                for lba in range(start_lba, end_lba):
                    result = self.read_lba(lba)
                    if result != value:
                        print("FAIL")
                        return
            print("PASS")
            return
        except Exception as e:
            print("FAIL")
            return False

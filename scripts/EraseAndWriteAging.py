from .BaseScript import BaseScript

class EraseAndWriteAging(BaseScript):
    def run(self):
        try:
            for loop in range(30):
                self.erase_lba(0, 3)
                for start_lba in range(2, 96, 2):
                    self.write_lba(start_lba, "0x00000001")
                    self.write_lba(start_lba, "0x00000002")
                    self.erase_lba(start_lba, 3)
                    for i in range(3):
                        if self.read_lba(start_lba + i) != '0x00000000':
                            return False
            return True

        except Exception as e:
            return False

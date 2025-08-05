import json, os

SSD_NAND_PATH = 'ssd_nand.txt'


class SSDController:
    def write(self, addr: int, val: str) -> bool:
        if self.is_invalid_input(addr, val):
            # OUTPUT 파일 ERROR 기입
            return False
        if not os.path.exists(SSD_NAND_PATH):
            with open(SSD_NAND_PATH, 'w') as f:
                json.dump({}, f)

        with open(SSD_NAND_PATH, "r") as f:
            memory = json.load(f)
            memory[str(addr)] = val.lower()

        with open(SSD_NAND_PATH, "w") as f:
            json.dump(memory, f)

        return True

    def _temp_read_for_test(self, addr: int):
        with open(SSD_NAND_PATH, "r") as f:
            return json.load(f).get(str(addr))

    def is_invalid_input(self, addr: int, val: str) -> bool:
        if not isinstance(addr, int):
            return True
        if addr < 0 or addr > 99:
            return True
        if not isinstance(val, str):
            return True
        if len(val) > 10:
            return True
        if not (val.startswith('0x') or val.startswith('0X')):
            return True
        if not set(val[2:]).issubset(set("0123456789abcdefABCDEF")):
            return True
        return False

    def check_output_msg(self):
        return 'ERROR'

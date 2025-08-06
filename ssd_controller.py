import json, os
import argparse

from validator import ControllerValidator

ERROR = 'ERROR'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SSD_NAND_PATH = os.path.join(PROJECT_ROOT, 'ssd_nand.txt')
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
DEFAULT_VALUE = '0x00000000'


class SSDController:
    def __init__(self):
        self.validator = ControllerValidator()

    def read(self, addr: int):
        if self.validator.is_lba_bad(addr):
            self.output(ERROR)
            return

        with open(SSD_NAND_PATH, "r", encoding="utf-8") as f:
            data = json.load(f).get(str(addr), DEFAULT_VALUE)
            self.output(data)

    def write(self, addr: int, val: str) -> bool:
        if self.validator.is_lba_bad(addr) or self.validator.is_value_bad(val):
            self.output(ERROR)
            return False

        self.update_nand_txt(addr, val)
        return True

    def update_nand_txt(self, addr, val):
        if not os.path.exists(SSD_NAND_PATH):
            with open(SSD_NAND_PATH, 'w') as f:
                json.dump({}, f)
        with open(SSD_NAND_PATH, "r") as f:
            memory = json.load(f)
            memory[str(addr)] = val.lower()
        with open(SSD_NAND_PATH, "w") as f:
            json.dump(memory, f)

    def _temp_read_for_test(self, addr: int):
        with open(SSD_NAND_PATH, "r") as f:
            return json.load(f).get(str(addr))

    def check_output_msg(self):
        with open(SSD_OUTPUT_PATH, 'r') as f:
            return f.read()

    def output(self, data):
        with open(SSD_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(data)
            
def main():
    parser = argparse.ArgumentParser(description="SSD Controller")
    parser.add_argument("mode", choices=["R", "W"], help="모드 선택: R(Read) 또는 W(Write)")
    parser.add_argument("address", type=int, help="LBA 주소 (0~99)")
    parser.add_argument("value", nargs="?", help="저장할 값 (0x로 시작하는 8자리 HEX, Write일 때만 사용)")

    args = parser.parse_args()
    controller = SSDController()
    # 동작 선택
    if args.mode == "R":
        controller.read(args.address)
    elif args.mode == "W":
        controller.write(args.address, args.value)


if __name__ == "__main__":
    main()

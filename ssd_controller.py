import json, os
import argparse

ERROR = 'ERROR'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SSD_NAND_PATH = os.path.join(PROJECT_ROOT, 'ssd_nand.txt')
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')


class SSDController:
    def __init__(self):
        ...

    def read(self, addr: int):
        try:
            if addr < 0 or addr > 99:
                raise Exception
            with open(SSD_NAND_PATH, "r", encoding="utf-8") as f:
                data = json.load(f).get(str(addr))
            self.output(data)
        except:
            self.output(ERROR)

    def write(self, addr: int, val: str) -> bool:
        if self.is_invalid_input(addr, val):
            self.output(ERROR)
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
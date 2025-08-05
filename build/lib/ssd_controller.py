import json
import argparse

ERROR = 'ERROR'
SSD_NAND_PATH = 'ssd_nand.txt'
SSD_OUTPUT_PATH = 'ssd_output.txt'
class SSDController:
    def __init__(self):
        ...
    def read(self,addr:int):
        if addr < 0 or addr > 99:
            self.output(ERROR)
            return
        with open(SSD_NAND_PATH, "r", encoding="utf-8") as f:
            data = json.load(f).get(str(addr))
        self.output(data)

    def output(self, data):
        with open(SSD_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(data)

    def write(self,addr, value):
        pass

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
        if args.value is None:
            print("ERROR: Write 모드에서는 값이 필요합니다.")
        elif not args.value.startswith("0x") or len(args.value) != 10:
            print("ERROR: 값은 0x로 시작하고 총 10자리 HEX이어야 합니다.")
        else:
            controller.write(args.address, args.value)

if __name__ == "__main__":
    main()
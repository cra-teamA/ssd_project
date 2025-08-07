import json, os
import argparse

from core.validator import ControllerValidator

ERROR = 'ERROR'
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SSD_NAND_PATH = os.path.join(PROJECT_ROOT, 'ssd_nand.txt')
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
DEFAULT_VALUE = '0x00000000'


class SSDController:
    def __init__(self):
        self.validator = ControllerValidator()

    def ssd_nand_init(self):
        with open(SSD_NAND_PATH, 'w') as f:
            json.dump({}, f)

    def read(self, addr: int) -> None:
        try:
            if self.validator.is_lba_bad(addr):
                self.output(ERROR)
                return
            with open(SSD_NAND_PATH, "r", encoding="utf-8") as f:
                data = json.load(f).get(str(addr), DEFAULT_VALUE)
                self.output(data)
        except FileNotFoundError:
            self.output(DEFAULT_VALUE)
        except json.decoder.JSONDecodeError:
            self.output(DEFAULT_VALUE)
        except Exception as e:
            print(e.__class__)
            self.output(ERROR)

    def write(self, addr: int, val: str) -> bool:
        try:
            if self.validator.is_lba_bad(addr) or self.validator.is_value_bad(val):
                self.output(ERROR)
                return False

            self.update_nand_txt(addr, val)
            return True
        except:
            self.output(ERROR)
            return False

    def update_nand_txt(self, addr, val) -> None:
        if not os.path.exists(SSD_NAND_PATH):
            self.ssd_nand_init()
        try:
            with open(SSD_NAND_PATH, "r") as f:
                memory = json.load(f)
                memory[str(addr)] = val.lower()
        except json.decoder.JSONDecodeError:
            self.ssd_nand_init()
        with open(SSD_NAND_PATH, "w") as f:
            json.dump(memory, f)

    def output(self, data):
        with open(SSD_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(data)

    def buffer_optimize(self, _cache, _buf_cmds):
        # TODO
        # 캐시에 버퍼 커맨드, 커맨드 재구성해보고  버퍼커맨드와 비교해서
        # 버퍼 커맨드에 엎어쓰 든지 하기
        optimized_cmd = []
        is_erase_duration = False
        s_addr = -1
        e_n = -1
        디폴트값 = '0x00000000'
        캐시사이즈 = 100
        for addr, val in _cache.items():
            if not val:
                if is_erase_duration:
                    is_erase_duration = False
                    optimized_cmd.append(('E', s_addr, e_n))
                continue

            if val != 디폴트값:
                if is_erase_duration:
                    is_erase_duration = False
                    optimized_cmd.append(('E', s_addr, e_n))

                optimized_cmd.append(('W', addr, val))

            if val == 디폴트값:
                if not is_erase_duration:
                    is_erase_duration = True
                    s_addr = addr
                    e_n = 1
                elif is_erase_duration:
                    e_n += 1
        return optimized_cmd


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

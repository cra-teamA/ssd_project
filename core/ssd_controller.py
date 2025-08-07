import json, os
import argparse

from core.validator import ControllerValidator
from core.command import Command, command_factory, DEFAULT_VALUE

ERROR = 'ERROR'
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SSD_NAND_PATH = os.path.join(PROJECT_ROOT, 'ssd_nand.txt')
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')


class SSDController:
    def __init__(self):
        self.validator = ControllerValidator()
        self.buffer = None
        # self.update_cache(self.buffer.get())
        self.update_cache(None)

    def update_cache(self, buffer):
        self.cache = {}
        if buffer is None:
            return self.cache
        for command in buffer:
            for i in range(command.size):
                self.cache[command.lba + i] = command.value
        return self.cache

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

    def erase(self, addr: int, size: int) -> bool:
        try:
            if self.validator.is_lba_bad(addr) or self.validator.is_size_bad(size):
                self.output(ERROR)
                return False

            self.update_nand_txt(addr, DEFAULT_VALUE, size=size)
            return True
        except:
            self.output(ERROR)
            return False

    def flush(self) -> bool:
        try:
            buffer = self.buffer.get()
            for command in buffer:
                self.run(command)
            self.buffer.truncate()
        except:
            self.output(ERROR)
            return False
    def update_nand_txt(self, addr, val, size=1) -> None:
        if not os.path.exists(SSD_NAND_PATH):
            self.ssd_nand_init()
        try:
            with open(SSD_NAND_PATH, "r") as f:
                memory = json.load(f)
                for i in range(size):
                    memory[str(addr + i)] = val.lower()
        except json.decoder.JSONDecodeError:
            self.ssd_nand_init()
        with open(SSD_NAND_PATH, "w") as f:
            json.dump(memory, f)


    def output(self, data):
        with open(SSD_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(data)
    def execute(self, command:Command):
        if command.command == "R":
            self.read(command.lba)
        elif command.command == "W":
            self.write(command.lba, command.value)
        elif command.command  == "E":
            self.erase(command.lba, command.size)
        elif command.command  == "F":
            self.flush()


def main():
    parser = argparse.ArgumentParser(description="SSD Controller")
    parser.add_argument("mode", choices=["R", "W", "E", "F"], help="모드 선택: R(Read) 또는 W(Write)")
    parser.add_argument("lba", type=int, nargs="?", help="LBA 주소 (0~99)")
    parser.add_argument("param", nargs="?", help="write일 경우 저장할 값 (0x로 시작하는 8자리 HEX), erase일 경우 삭제할 size")

    controller = SSDController()
    controller.execute(command_factory(parser.parse_args()))

if __name__ == "__main__":
    main()

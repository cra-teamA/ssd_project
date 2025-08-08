import json, os
import argparse

from core.validator import ControllerValidator
from core.command import Command, command_factory, DEFAULT_VALUE, EraseCommand, WriteCommand
from core.command_buffer import CommandBuffer

ERROR = 'ERROR'
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SSD_NAND_PATH = os.path.join(PROJECT_ROOT, 'ssd_nand.txt')
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')


class SSDController:
    def __init__(self):
        self.validator = ControllerValidator()
        self.buffer = CommandBuffer()
        self.update_cache(self.buffer.get())

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
                self.execute(command)
            self.buffer.truncate()
        except:
            self.output(ERROR)
            return False

    def buffer_optimize(self):
        generated_commands = self._generate_commands()
        picked_cmd = self._pick_smaller_commands(generated_commands, self.buffer.get())
        self.buffer.replace(picked_cmd)

    def _pick_smaller_commands(self, generated_commands, _buf_cmds):
        if len(generated_commands) < len(_buf_cmds):
            return generated_commands
        return _buf_cmds

    def _generate_commands(self):
        optimized_cmd = []
        is_erase_duration = False
        s_addr = -1
        e_n = -1
        for addr, val in self.cache.items():
            if not val:
                if is_erase_duration:
                    is_erase_duration = False
                    optimized_cmd.append(EraseCommand('E', s_addr, e_n))
                continue

            if val != DEFAULT_VALUE:
                if is_erase_duration:
                    is_erase_duration = False
                    optimized_cmd.append(EraseCommand('E', s_addr, e_n))
                optimized_cmd.append(WriteCommand('W', addr, val))

            else:
                if is_erase_duration:
                    e_n += 1
                else:
                    is_erase_duration = True
                    s_addr = addr
                    e_n = 1
        return optimized_cmd

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

    def check_output_msg(self):
        with open(SSD_OUTPUT_PATH, 'r') as f:
            return f.read()

    def output(self, data):
        with open(SSD_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(data)

    def execute(self, command: Command):
        if command.mode == "R":
            self.read(command.lba)
        elif command.mode == "W" or command.mode == "E":
            if self.buffer.is_full():
                self.flush()
            self.buffer.add(command)
            self.buffer_optimize()
            self.buffer.syncToDirectory()
        elif command.mode == "F":
            self.flush()


def main():
    parser = argparse.ArgumentParser(description="SSD Controller")
    parser.add_argument("mode", choices=["R", "W", "E", "F"], help="모드 선택: R(Read) 또는 W(Write)")
    parser.add_argument("lba", type=int, nargs="?", help="LBA 주소 (0~99)")
    parser.add_argument("param", nargs="?", help="write일 경우 저장할 값 (0x로 시작하는 8자리 HEX), erase일 경우 삭제할 size")

    controller = SSDController()
    controller.execute(command_factory(**vars(parser.parse_args())))


if __name__ == "__main__":
    main()




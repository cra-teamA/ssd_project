from abc import ABC, abstractmethod
import sys, os
import subprocess
from xmlrpc.client import FastParser

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logger import Logger

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

MIN_LBA = 0
MAX_LBA = 99
MAX_VALUE_LENGTH = 10
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
SSD_COMMAND = os.path.join(PROJECT_ROOT, 'ssd.bat')


class Command(ABC):
    def __init__(self, read_command):
        self.logger = Logger()
        _, = read_command.split()

    def run(self):
        self.logger.set_log("Run")
        self.execute()
        self.logger.set_log("Done")

    def run_ssd_command(self, *args):
        subprocess.run([SSD_COMMAND, *map(str, args)])

    def _is_invalid_lba(self, lba: str) -> bool:
        if int(lba) < MIN_LBA or int(lba) > MAX_LBA:
            self.logger.set_log("Invalid LBA")
            return True
        return False

    def _is_invalid_value(self, value: str) -> bool:
        if len(value) > MAX_VALUE_LENGTH or not value.upper().startswith("0X"):
            self.logger.set_log("Invalid Value")
            return True
        return False

    @abstractmethod
    def execute(self):
        pass


class Read(Command):
    def __init__(self, read_command: str, is_script: bool = False):
        self.logger = Logger()
        self.return_value = None
        _, lba = read_command.split()
        self.lba = lba
        self.is_script = is_script

    def execute(self):
        if self._is_invalid_lba(self.lba):
            raise ValueError
        self.run_ssd_command("R", self.lba)
        with open(SSD_OUTPUT_PATH, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
        self.logger.set_log_with_print(f"[Read] LBA {self.lba} : {line}", self.is_script)
        self.return_value = line

class FullRead(Command):
    def execute(self):
        self.logger.set_log_with_print('[Full Read]')
        for lba in range(MIN_LBA, MAX_LBA + 1):
            self.run_ssd_command("R", lba)
            with open(SSD_OUTPUT_PATH, 'r', encoding='utf-8') as f:
                line = f.readline().strip()
            self.logger.set_log_with_print(f'LBA {lba:02d} : {line}')

class Help(Command):
    def execute(self):
        print('''
        제작자: [Team All Clear] 장진섭 팀장, 박성일, 이규홍, 최준식, 임소현, 이휘은
        명령어 사용 법 :
         1. read: read [LBA]
         2. write: write [LBA] [VALUE]
         3. fullwrite: fullwrite [VALUE]
         4. fullread: fullread
         5. 1_FullWriteAndReadCompare: 1_ 혹은 1_FullWriteAndReadCompare 입력
         6. 2_PartialLBAWrite: 2_ 혹은 2_PartialLBAWrite 입력
         7. 3_WriteReadAging: 3_ 혹은 3_WriteReadAging 입력
         8. 4_EraseAndWriteAging: 4_ 혹은 4_EraseAndWriteAging 입력
         9. help: help
         10. exit: exit
         11. flush: flush
         12. erase: erase [LBA] [SIZE]
         13. erase_range: erase_range [START_LBA] [END_LBA]
        그 외 명령어 입력 시, INVALID COMMAND 가 출력 됩니다.'''
              )


class Exit(Command):
    def execute(self):
        self.logger.set_log_with_print("Exiting shell...")
        sys.exit(0)

class Write(Command):
    def __init__(self, read_command: str, is_script: bool = False):
        self.logger = Logger()
        _, lba, value = read_command.split()
        self.lba = lba
        self.value = value
        self.is_script = is_script

    def execute(self):
        if self._is_invalid_lba(self.lba):
            raise ValueError
        if self._is_invalid_value(self.value):
            raise ValueError
        self.run_ssd_command("W", self.lba, f"0x{int(self.value, 16) :08X}")
        self.logger.set_log_with_print("[Write] Done", self.is_script)


class FullWrite(Command):
    def __init__(self, read_command: str):
        self.logger = Logger()
        _, value = read_command.split()
        self.value = value

    def execute(self):
        if self._is_invalid_value(self.value):
            raise ValueError
        for lba in range(MIN_LBA, MAX_LBA + 1):
            self.run_ssd_command("W", lba, f"0x{int(self.value, 16) :08X}")
        self.logger.set_log_with_print("[FullWrite] Done")


class Erase(Command):
    def __init__(self,read_command: str, is_script: bool = False):
        self.logger = Logger()
        _, lba, size = read_command.split()
        self.lba = lba
        self.size = size
        self.is_script = is_script

    def execute(self):
        if self._is_invalid_lba(self.lba):
            self.logger.set_log("invalid lba")
            raise ValueError
        start, size = int(self.lba), int(self.size)  # int 아니면 Value Error
        # size가 음일때 start 바꿔주기
        if size < 0:
            new_start = max(MIN_LBA, start + size + 1)
            new_size = min(start, abs(size))
            start, size = new_start, new_size
        end = min(start + size - 1, MAX_LBA)
        size = end - start + 1
        self.logger.set_log_with_print(f'[erase] lba {start} | size {size}', self.is_script)
        self._erase(start, size)

    def _erase(self, lba: int, size: int, label: str = None):
        if label:
            print(f"{label} lba {lba} | size {size}")
        while size > 0:
            chunk = min(size, MAX_VALUE_LENGTH)
            self.run_ssd_command("E", lba, chunk)
            lba += chunk
            size -= chunk

class EraseRange(Erase):
    def __init__(self,read_command: str, is_script: bool = False):
        self.logger = Logger()
        _, start_lba, end_lba = read_command.split()
        self.start_lba = start_lba
        self.end_lba = end_lba
        self.is_script = is_script

    def execute(self):
        if self._is_invalid_lba(self.start_lba) or self._is_invalid_lba(self.end_lba):
            self.logger.set_log("invalid lba")
            raise ValueError
        start, end = sorted((int(self.start_lba), int(self.end_lba)))
        start = max(start, MIN_LBA)
        end = min(end, MAX_LBA)
        size = end - start + 1
        self.logger.set_log_with_print(f'[erase range] lba {start} | size {size}', self.is_script)
        self._erase(start, size)

class Flush(Command):
    def execute(self):
        self.run_ssd_command("F")




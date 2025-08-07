import os
import subprocess
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logger import Logger
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from scripts.ScriptRunner import ScriptRunner

MIN_LBA = 0
MAX_LBA = 99
MAX_VALUE_LENGTH = 10
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
SSD_COMMAND = os.path.join(PROJECT_ROOT, 'ssd.bat')


class Shell:
    def __init__(self):
        self.logger = Logger()

    def read(self, read_command: str, is_script: bool = False):
        self.logger.set_log(f"[Read] get {read_command}")
        _, lba = read_command.split()
        if self._is_invalid_lba(lba):
            self.logger.set_log("invalid_lba")
            raise ValueError
        self.run_ssd_command("R", lba)
        with open(SSD_OUTPUT_PATH, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
        if not is_script:
            print(f"[Read] LBA {lba} : {line}")
        return line

    def fullread(self, read_command: str):
        self.logger.set_log(f"[Full Read] get {read_command}")
        if len(read_command.split()) != 1:
            self.logger.set_log(f"[Full Read] cmd argument is not valid")
            raise ValueError
        print('[Full Read]')
        for lba in range(MIN_LBA, MAX_LBA + 1):
            self.run_ssd_command("R", lba)
            with open(SSD_OUTPUT_PATH, 'r', encoding='utf-8') as f:
                line = f.readline().strip()
            result = f'LBA {lba:02d} : {line}'
            print(result)
            self.logger.set_log(result)

    def help(self, read_command: str):
        self.logger.set_log(f"[Help] get {read_command}")
        if len(read_command.split()) != 1:
            self.logger.set_log(f"[Help] cmd argument is not valid")
            raise ValueError
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

    def exit(self, read_command: str):
        self.logger.set_log(f"[Exit] get {read_command}")
        if len(read_command.split()) != 1:
            raise ValueError
        print("Exiting shell...")
        sys.exit(0)

    def write(self, read_command: str, is_script: bool = False):
        self.logger.set_log(f"[Write] get {read_command}")
        _, lba, value = read_command.split()
        if self._is_invalid_lba(lba):
            self.logger.set_log(f"invalid_lba")
            raise ValueError
        if self._is_invalid_value(value):
            self.logger.set_log(f"invalid_value")
            raise ValueError
        self.run_ssd_command("W", lba, f"0x{int(value, 16) :08X}")
        result = "[Write] Done"
        if not is_script:
            print(result)
        self.logger.set_log(result)

    def fullwrite(self, read_command: str):
        self.logger.set_log(f"[Full write] get {read_command}")
        _, value = read_command.split()

        if self._is_invalid_value(value):
            self.logger.set_log(f"invalid_value")
            raise ValueError
        for lba in range(MIN_LBA, MAX_LBA + 1):
            self.run_ssd_command("W", lba, f"0x{int(value, 16) :08X}")
        result = "[FullWrite] Done"
        print(result)
        self.logger.set_log(result)

    def erase(self, read_command: str, is_script: bool = False):
        self.logger.set_log(f"[Erase] get {read_command}")
        _, lba, size = read_command.split()
        if self._is_invalid_lba(lba):
            self.logger.set_log("invalid lba")
            raise ValueError
        start, size = int(lba), int(size)  # int 아니면 Value Error
        # size가 음일때 start 바꿔주기
        if size < 0:
            new_start = max(MIN_LBA, start + size + 1)
            new_size = min(start, abs(size))
            start, size = new_start, new_size
        end = min(start + size - 1, MAX_LBA)
        size = end - start + 1
        result = f'[erase] lba {start} | size {size}'
        if not is_script:
            print(result)
        self.logger.set_log("result")
        self._erase(start, size)

    def erase_range(self, read_command: str, is_script: bool = False):
        self.logger.set_log(f"[Erase range] get {read_command}")
        _, start_lba, end_lba = read_command.split()
        if self._is_invalid_lba(start_lba) or self._is_invalid_lba(end_lba):
            self.logger.set_log("invalid lba")
            raise ValueError
        start, end = sorted((int(start_lba), int(end_lba)))
        start = max(start, MIN_LBA)
        end = min(end, MAX_LBA)
        size = end - start + 1
        result = f'[erase range] lba {start} | size {size}'
        if not is_script:
            print(result)
        self.logger.set_log(result)
        self._erase(start, size)

    def _erase(self, lba: int, size: int, label: str = None):
        if label:
            print(f"{label} lba {lba} | size {size}")
        while size > 0:
            chunk = min(size, MAX_VALUE_LENGTH)
            self.run_ssd_command("E", lba, chunk)
            lba += chunk
            size -= chunk

    def flush(self, command):
        if len(command.split()) != 1:
            raise ValueError
        else:
            self.run_ssd_command("F")

    def _is_invalid_lba(self, lba: str) -> bool:
        return int(lba) < MIN_LBA or int(lba) > MAX_LBA

    def _is_invalid_value(self, value: str) -> bool:
        return len(value) > MAX_VALUE_LENGTH or not value.upper().startswith("0X")

    def run_script(self, command):
        runner = ScriptRunner(self)
        runner.run(command)

    def run_ssd_command(self,*args):
        subprocess.run([SSD_COMMAND, *map(str, args)])


def shell_command_mode(shell: Shell):
    COMMAND_MAP = {
        "read": shell.read,
        "write": shell.write,
        "fullread": shell.fullread,
        "fullwrite": shell.fullwrite,
        "erase": shell.erase,
        "erase_range": shell.erase_range,
        "flush": shell.flush,
        "help": shell.help,
        "exit": shell.exit,
    }
    while True:
        command = input("Shell > ").strip()
        if not command:
            continue
        cmd_name = command.split()[0]
        handler = COMMAND_MAP.get(cmd_name, shell.run_script)
        try:
            handler(command)
        except ValueError:
            print("INVALID COMMAND")


def main():
    shell = Shell()
    if len(sys.argv) == 1:
        shell_command_mode(shell)
    else:
        shell.run_script(f"shell {sys.argv[1]}")


if __name__ == "__main__":
    main()

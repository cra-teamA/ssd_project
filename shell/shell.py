import os
import subprocess
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from scripts.ScriptRunner import ScriptRunner

MIN_LBA = 0
MAX_LBA = 99
MAX_VALUE_LENGTH = 10
ERROR = "ERROR"
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
SSD_COMMAND = os.path.join(PROJECT_ROOT, 'ssd.bat')


class Shell:
    def __init__(self):
        ...

    def read(self, read_command:str, is_script: bool = False):
        _, lba = read_command.split()
        if self._is_invalid_lba(lba):
            raise ValueError
        line = self._read(lba)
        if not is_script:
            if line == ERROR:
                print(f"[Read] {ERROR}")
            else:
                print(f"[Read] LBA {lba} : {line}")
        return line

    def _read(self, lba):
        subprocess.run(
            [SSD_COMMAND, "R", lba],
            capture_output=True,
            text=True
        )
        output = SSD_OUTPUT_PATH
        with open(output, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
        return line

    def fullread(self, read_command: str):
        if len(read_command.split()) != 1:
            raise ValueError
        print('[Full Read]')
        for lba in range(MIN_LBA, MAX_LBA + 1):
            print(f'LBA {lba:02d} : {self._read(str(lba))}')

    def help(self, read_command: str):
        if len(read_command.split()) != 1:
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
         8. exit: exit
        그 외 명령어 입력 시, INVALID COMMAND 가 출력 됩니다.'''
              )

    def exit(self, read_command:str):
        if len(read_command.split()) != 1:
            raise ValueError
        print("Exiting shell...")
        sys.exit(0)

    def get_lba_from_read_command(self, read_command: str) -> str:
        lba = read_command.split()[1]
        return lba

    def write(self, read_command: str, is_script: bool = False):
        _, lba, value = read_command.split()
        if self._is_invalid_lba(lba):
            raise ValueError
        if self._is_invalid_value(value):
            raise ValueError
        subprocess.run([SSD_COMMAND, "W", lba, f"0x{int(value, 16) :08X}"])

        if not is_script:
            print("[Write] Done")

    def fullwrite(self, read_command: str):
        _, value = read_command.split()

        if self._is_invalid_value(value):
            raise ValueError
        for lba in range(MIN_LBA, MAX_LBA + 1):
            subprocess.run([SSD_COMMAND, "W", str(lba), f"0x{int(value, 16) :08X}"])
        print("[FullWrite] Done")

    def _is_invalid_lba(self, lba: str) -> bool:
        return int(lba) < MIN_LBA or int(lba) > MAX_LBA

    def _is_invalid_value(self, value: str) -> bool:
        return len(value) > MAX_VALUE_LENGTH or not value.upper().startswith("0X")

    def run_script(self, command):
        runner = ScriptRunner(self)
        result = runner.run(command)

        if result is True:
            print("PASS")
        elif result is False:
            print("FAIL")

def main():
    shell = Shell()
    while (1):
        command = input("Shell > ")
        try:
            command_prefix = command.split()[0]
            if command_prefix == "write":
                shell.write(command)
            elif command_prefix == "read":
                shell.read(command)
            elif command_prefix == "fullwrite":
                shell.fullwrite(command)
            elif command_prefix == "fullread":
                shell.fullread(command)
            elif command_prefix == "help":
                shell.help(command)
            elif command_prefix == "exit":
                shell.exit(command)
            else:
                shell.run_script(command)
        except ValueError:
            print("INVALID COMMAND")

if __name__ == "__main__":
    main()

import subprocess
import sys

MIN_LBA = 0
MAX_LBA = 99
MAX_VALUE_LENGTH = 10
ERROR = "ERROR"
VALID_COMMAND = ["write", "read", "exit", "help", "exit", "fullwrite", "fullread", "1_", "2_", "3_",
                 "1_FullWriteAndReadCompare", "2_PartialLBAWrite", "3_WriteReadAging"]


class Shell:
    def __init__(self):
        ...

    def read(self, read_command):
        parts = read_command.split()
        if len(parts) != 2:
            raise ValueError
        lba = self.get_lba_from_read_command(read_command)
        if self._is_invalid_lba(lba):
            raise ValueError
        line = self._read(lba)
        if line == ERROR:
            print(f"[Read] {ERROR}")
        else:
            print(f"[Read] LBA {lba} : {line}")
        return line

    def _read(self, lba):
        subprocess.run(
            ["ssd", "R", lba],
            capture_output=True,
            text=True
        )
        output = 'ssd_output.txt'
        with open(output, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
        return line

    def full_read(self):
        print('[Full Read]')
        for lba in range(MIN_LBA, MAX_LBA + 1):
            print(f'LBA {lba:02d} : {self._read(lba)}')

    def help(self):
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

    def exit(self):
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
        subprocess.run(["ssd", "W", lba, f"0x{int(value, 16) :08X}"])

        if not is_script:
            print("[Write] Done")

    def fullwrite(self, read_command: str):
        _, value = read_command.split()

        if self._is_invalid_value(value):
            raise ValueError
        for lba in range(MIN_LBA, MAX_LBA + 1):
            subprocess.run(["ssd", "W", str(lba), f"0x{int(value, 16) :08X}"])
        print("[FullWrite] Done")

    def _is_invalid_lba(self, lba: str) -> bool:
        return int(lba) < MIN_LBA or int(lba) > MAX_LBA

    def _is_invalid_value(self, value: str) -> bool:
        return len(value) > MAX_VALUE_LENGTH or not value.upper().startswith("0X")


def is_valid_command():
    cli = input("Shell > ")
    if not cli.startswith(tuple(VALID_COMMAND)):
        print("INVALID COMMAND")
        return False
    return True

import subprocess

MIN_LBA = 0
MAX_LBA = 99
MAX_VALUE_LENGTH = 10


class Shell:
    def __init__(self):
        ...

    def read(self, read_command):
        lba = self.get_lba_from_read_command(read_command)
        subprocess.run(
            ["ssd", "R", lba],
            capture_output=True,
            text=True
        )
        output = 'ssd_output.txt'
        with open(output, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
        if line == "ERROR":
            print("[Read] ERROR")
        else:
            print(f"[Read] LBA {lba} : {line}")

    def help(self):
        message = '''
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
        print(message)

    def get_lba_from_read_command(self, read_command: str) -> str:
        lba = read_command.split()[1]
        return lba

    def write(self, read_command: str):
        _, lba, value = read_command.split()
        try:
            if int(lba) < MIN_LBA or int(lba) > MAX_LBA:
                raise ValueError
            if len(value) > MAX_VALUE_LENGTH or not value.upper().startswith("0X"):
                raise ValueError
            subprocess.run(["ssd", "W", lba, f"0x{int(value, 16) :08X}"])
            print("[Write] Done")
        except ValueError:
            print("INVALID COMMAND")
            return

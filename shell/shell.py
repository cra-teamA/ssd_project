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

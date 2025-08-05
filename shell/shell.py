import subprocess


class Shell:
    def __init__(self):
        ...

    def read(self, read_command):
        lba = self.get_lba_from_read_command(read_command)
        subprocess.run(
            ["python", "ssd.py", "R", lba],
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

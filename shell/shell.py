import subprocess


class Shell:
    def __init__(self):
        ...

    def read(self, command_lba):
        lba = 3
        subprocess.run(
            ["python", "ssd.py", "R", str(lba)],
            capture_output=True,
            text=True
        )
        output = 'ssd_output.txt'
        with open(output, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
        print(f"[Read] LBA {lba} : {line}")

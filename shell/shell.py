import subprocess


class Shell:
    def __init__(self):
        ...

        subprocess.run(
            capture_output=True,
            text=True
        )
        output = 'ssd_output.txt'
        with open(output, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
        print(f"[Read] LBA {lba} : {line}")

import subprocess

MIN_ADDRESS = 0
MAX_ADDRESS = 99
MAX_DATA_LENGTH = 10


class Shell:
    def __init__(self):
        ...

    def read(self, read_command):
        lba = self.get_lba_from_read_command(read_command)
        subprocess.run(
            [ "ssd", "R", lba],
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

    def write(self, lba: str):
        cmd, address, data = lba.split()
        if int(address) < MIN_ADDRESS or int(address) > MAX_ADDRESS:
            print("INVALID COMMAND")
            return
        if len(data) > MAX_DATA_LENGTH:
            print("INVALID COMMAND")
            return
        data_num = int(data, 16)
        data = f"0x{data_num:08X}"
        subprocess.run(["ssd", "W", address, data])
        print("[Write] Done")

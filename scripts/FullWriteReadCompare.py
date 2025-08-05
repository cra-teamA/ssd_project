from scripts.BaseScript import BaseScript
from shell.shell import Shell

class FullWriteReadCompare(BaseScript):
    def __init__(self, shell_interface:Shell):
        self.shell = shell_interface


    def run(self):
        for i in range(100):
            self.shell.write(f"W {i} 0x00000000")

        command = "R 0"
        self.shell.read(command)
from scripts.BaseScript import BaseScript
from shell.shell import Shell

class FullWriteReadCompare(BaseScript):
    def __init__(self, shell_interface:Shell):
        self.shell = shell_interface


    def run(self):
        command = "W 1 0x00000000"
        self.shell.write(command)

        command = "R 0"
        self.shell.read(command)
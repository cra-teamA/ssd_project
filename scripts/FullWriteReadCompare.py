from scripts.BaseScript import BaseScript
from shell.shell import Shell

class FullWriteReadCompare(BaseScript):
    def __init__(self, shell_interface:Shell):
        self.shell = shell_interface


    def run(self):
        self.shell.read(0)
        self.shell.write(1,"0x00000000")
        pass
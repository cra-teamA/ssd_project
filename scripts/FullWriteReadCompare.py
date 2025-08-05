from scripts.BaseScript import BaseScript
from shell.shell import Shell

class Script1_FullWrite(BaseScript):
    def __init__(self, shell_interface:Shell):
        self.shell = shell_interface


    def run(self):
        self.shell.read(0)

        pass
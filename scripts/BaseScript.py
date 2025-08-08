from abc import ABC, abstractmethod
from shell.shell_command import Write,Read,Erase

class BaseScript(ABC):

    def __init__(self):
        self.isCommandFromScript = True

    def write_lba(self, lba : int, data : str):
        cmd = f"write {lba} {data}"
        write_command = Write(cmd,self.isCommandFromScript)
        write_command.run()

    def read_lba(self, lba : int):
        cmd = f"read {lba}"
        read_command = Read(cmd,self.isCommandFromScript)
        read_command.run()
        return read_command.result

    def erase_lba(self, lba : int, size : int):
        cmd = f"erase {lba} {size}"
        erase_command = Erase(cmd, self.isCommandFromScript)
        erase_command.run()

    @abstractmethod
    def run(self):
        pass
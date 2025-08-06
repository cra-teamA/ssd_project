from abc import ABC, abstractmethod

class BaseScript(ABC):

    def __init__(self, shell_interface):
        self.shell = shell_interface  # read/write interface
        self.isCommandFromScript = True

    def write_lba(self, lba : str, data : str):
        cmd = f"write {lba} {data}"
        self.shell.write(cmd,self.isCommandFromScript)

    def read_lba(self, lba: str):
        cmd = f"read {lba}"
        return self.shell.read(cmd,self.isCommandFromScript)

    @abstractmethod
    def run(self):
        pass
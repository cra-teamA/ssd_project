from abc import ABC, abstractmethod
from shell.shell import Shell


class BaseScript(ABC):
    def __init__(self, shell_interface : Shell):
        self.shell = shell_interface  # read/write interface

    def write_lba(self, lba : str, data : str):
        cmd = f"write {lba} {data}"
        self.shell.write(cmd)

    def read_lba(self, lba: str):
        cmd = f"read {lba}"
        return self.shell.read(cmd)

    @abstractmethod
    def run(self):
        pass
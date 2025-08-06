from abc import ABC, abstractmethod

class BaseScript(ABC):
    def __init__(self, shell_interface):
        self.shell = shell_interface  # read/write interface

    def write_lba(self, lba, data):
        self.shell.write(lba, data)

    def read_lba(self, lba):
        return self.shell.read(lba)

    @abstractmethod
    def run(self):
        pass
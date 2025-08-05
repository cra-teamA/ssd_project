from abc import ABC, abstractmethod

class BaseScript(ABC):
    def __init__(self, nand_interface):
        self.nand = nand_interface  # read/write interface

    @abstractmethod
    def run(self):
        pass
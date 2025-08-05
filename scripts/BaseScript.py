from abc import ABC, abstractmethod

class BaseScript(ABC):
    def __init__(self, shell_interface):
        self.shell = shell_interface  # read/write interface

    @abstractmethod
    def run(self):
        pass
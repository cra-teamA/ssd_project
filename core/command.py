from abc import ABC

DEFAULT_VALUE = '0x00000000'

class Command(ABC):
    mode: str
    lba: int
    size: int
    value: str = None  # 기본값 None
    def __init__(self, *args):
        ...
class ReadCommand(Command):
    def __init__(self, *args):
        self.mode = args[0]
        self.lba = args[1]
class WriteCommand(Command):
    def __init__(self, *args):
        self.mode = args[0]
        self.lba = args[1]
        self.value = args[2]
        self.size = 1

    def __eq__(self, other):
        if not isinstance(other, WriteCommand):
            return False
        return self.mode == other.mode and self.lba == other.lba and self.size == other.size and self.value == other.value


class EraseCommand(Command):
    def __init__(self, *args):
        self.mode = args[0]
        self.lba = args[1]
        self.value = DEFAULT_VALUE
        self.size = int(args[2])
    def __eq__(self, other):
        if not isinstance(other, EraseCommand):
            return False
        return self.mode == other.mode and self.lba == other.lba and self.size == other.size and self.value == other.value

class FlushCommand(Command):
    def __init__(self, *args):
        self.mode = args[0]
def command_factory(mode, lba, param):

    if mode == 'F':
        return FlushCommand(mode)
    if mode == 'R':
        return ReadCommand(mode, lba)
    if mode == 'W':
        return WriteCommand(mode, lba, param)
    if mode == 'E':
        return EraseCommand(mode, lba, param)

    raise ValueError("Invalid arguments for Command")
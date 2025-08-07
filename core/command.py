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
        self.command = args[0]
        self.lba = args[1]
class WriteCommand(Command):
    def __init__(self, *args):
        self.command = args[0]
        self.lba = args[1]
        self.value = args[2]
        self.size = 1

    def __eq__(self, other):
        if not isinstance(other, WriteCommand):
            return False
        return self.command == other.command and self.lba == other.lba and self.size == other.size and self.value == other.value


class EraseCommand(Command):
    def __init__(self, *args):
        self.command = args[0]
        self.lba = args[1]
        self.value = DEFAULT_VALUE
        self.size = args[2]
    def __eq__(self, other):
        if not isinstance(other, EraseCommand):
            return False
        return self.command == other.command and self.lba == other.lba and self.size == other.size and self.value == other.value

class FlushCommand(Command):
    def __init__(self, *args):
        self.command = args[0]
def command_factory(args):
    if args.mode == 'F':
        return FlushCommand(args.mode)
    if args.mode == 'R':
        return ReadCommand(args.mode, args.lba)
    if args.mode == 'W':
        return WriteCommand(args.mode, args.lba, args.param)
    if args.mode == 'E':
        return EraseCommand(args.mode, args.lba, args.param)

    raise ValueError("Invalid arguments for Command")
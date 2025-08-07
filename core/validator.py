from abc import ABC, abstractmethod


class Validator(ABC):
    ADDR_MIN = 0
    ADDR_MAX = 99
    SIZE_MIN = 0
    SIZE_MAX = 10

    @abstractmethod
    def is_lba_bad(self, lba) -> bool:
        pass

    @abstractmethod
    def is_value_bad(self, val) -> bool:
        pass


class ControllerValidator(Validator):
    def is_lba_bad(self, lba) -> bool:
        if not isinstance(lba, int):
            return True
        if lba < self.ADDR_MIN or lba > self.ADDR_MAX:
            return True
        return False
    def is_size_bad(self, size) -> bool:
        if not isinstance(size, int):
            return True
        if size < self.SIZE_MIN or size > self.SIZE_MAX:
            return True
        return False

    def is_value_bad(self, val) -> bool:
        if not isinstance(val, str):
            return True
        if len(val) != 10:
            return True
        if not (val.startswith('0x') or val.startswith('0X')):
            return True
        if not set(val[2:]).issubset(set("0123456789abcdefABCDEF")):
            return True
        return False

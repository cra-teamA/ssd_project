from abc import ABC, abstractmethod


class Validator(ABC):
    ADDR_MIN = 0
    ADDR_MAX = 99

    @abstractmethod
    def check_lba(self, lba) -> bool:
        pass

    @abstractmethod
    def check_value(self, val) -> bool:
        pass


class ControllerValidator(Validator):
    def check_lba(self, lba) -> bool:
        if not isinstance(lba, int):
            return True
        if lba < self.ADDR_MIN or lba > self.ADDR_MAX:
            return True
        return False

    def check_value(self, val) -> bool:
        if not isinstance(val, str):
            return True
        if len(val) != 10:
            return True
        if not (val.startswith('0x') or val.startswith('0X')):
            return True
        if not set(val[2:]).issubset(set("0123456789abcdefABCDEF")):
            return True
        return False

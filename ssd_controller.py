class SSDController:
    def write(self, addr: int, val: str) -> bool:

        if self.is_invalid_input(addr, val):
            return False

        return True

    def is_invalid_input(self, addr, val):
        if not isinstance(addr, int):
            return True
        if addr < 0 or addr > 99:
            return True
        if not isinstance(val, str):
            return True
        if len(val) > 10:
            return True
        if not (val.startswith('0x') or val.startswith('0X')):
            return True
        if not set(val[2:]).issubset(set("0123456789abcdef")):
            return True
        return False

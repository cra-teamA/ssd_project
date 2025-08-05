class SSDController:
    def write(self, addr: int, val: str) -> bool:
        if not isinstance(addr, int):
            return False
        if addr < 0 or addr > 99:
            return False
        if not isinstance(val, str):
            return False
        if not val.startswith('0x'):
            return False
        if any([char not in '0123456789abcdef' for char in val[2:]]):
            return False

        return True

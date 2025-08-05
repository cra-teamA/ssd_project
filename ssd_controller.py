class SSDController:
    def write(self, addr: int, val: str) -> bool:
        if not isinstance(addr, int):
            return False
        if addr < 0 or addr > 99:
            return False
        if not isinstance(val, str):
            return False
        if len(val) > 10:
            return False

        val = val.lower()

        if not val.startswith('0x'):
            return False
        if any([char not in '0123456789abcdef' for char in val]):
            return False

        return True

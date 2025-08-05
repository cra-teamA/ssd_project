class SSDController:
    def write(self, addr: int, val: str) -> bool:
        if not isinstance(addr, int):
            return False
        if addr < 0 or addr > 99:
            return False
        if not isinstance(val, str):
            return False
        return True

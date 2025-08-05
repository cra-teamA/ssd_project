class SSDController:
    def write(self, addr: int, val: str) -> bool:
        if addr > 99 :
            return False
        return True

import os
class SSDController:
    def read(self,addr):
        filepath = 'ssd_nand.txt'
        if not os.path.exists(filepath):
            with open(filepath,'w') as f:
                f.write('{}')

        with open(filepath, 'r') as f:  # 읽기
            dic = eval(f.read())
            return dic.get(addr,0)

    def write(self,addr, value):
        pass
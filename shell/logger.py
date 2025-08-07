
import datetime
import os
import inspect
import re

MAX_FILE_SIZE = 10 * 1024 #10kb
TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

class Logger:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self._init_file()


    def _init_file(self):
        self.log_file = "latest.log"

        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'):
                pass

    
    def _get_caller_info(self):
        stack = inspect.stack()
        # stack[0] : 현재 함수(get_caller_info)
        # stack[1] : 이 함수를 호출한 곳 (ex: Logger.print)
        # stack[2] : Logger.print를 호출한 곳(원하는 정보)
        
        if len(stack) < 3:
            return None
        
        frame = stack[2]
        frame_info = inspect.getframeinfo(frame[0])

        func_name = frame_info.function
        filename = frame_info.filename
        lineno = frame_info.lineno

        cls_name = None
        local_vars = frame.frame.f_locals
        if 'self' in local_vars:
            cls_name = type(local_vars['self']).__name__

        return cls_name, func_name, filename, lineno
        
    
    def info(self, message: str):
        cls_name, func_name, _, _ = self._get_caller_info()
        time_stamp = datetime.datetime.now().strftime(TIME_STAMP_FORMAT)
        caller = f"{cls_name}.{func_name}"
        log = f"[INFO][{time_stamp}] {caller:30} {message}"
        self._logging(log)
        

    def _logging(self, log_message: str):
        if self._check_log_file_size_max():
            self._change_log_file_name()
        print(log_message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def _check_log_file_size_max(self):
        if not os.path.exists(self.log_file):
            return False
        if os.path.getsize(self.log_file)> MAX_FILE_SIZE:
            return True
        return False
    
    def _change_log_file_name(self):
        with open(self.log_file, 'rb') as f:
            f.seek(-2, os.SEEK_END)  # 파일 끝에서 시작
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
        
        match = re.search(r'\[(INFO|DEBUG|ERROR)?\]?\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', last_line)
        if not match:
            print("No valid timestamp found in last line.")
            return
        
        dt = datetime.datetime.strptime(match.group(2),TIME_STAMP_FORMAT)
        last_log_time = dt.strftime("%Y%m%d_%Hh_%Mm_%Ss")
        new_name = f"until_{last_log_time}.log"
        os.rename(self.log_file, new_name)




class AAA:
    def __init__(self):
        self.num = 1
        self.logger = Logger()

    def a(self):
        self.logger.info(f"aaa {self.num}")
        self.num+=1


class BBB:
    def __init__(self):
        self.num = 100
        self.logger = Logger()

    def b(self):
        self.logger.info(f"bbb {self.num}")
        self.num -= 1


def main():
    a = AAA()
    b = BBB()

    a.a()
    a.a()
    b.b()
    b.b()
    a.a()
    b.b()

if __name__ == "__main__":
    main()



    
    

    
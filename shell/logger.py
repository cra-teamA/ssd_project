
import datetime
import os
import inspect

MAX_FILE_SIZE = 10  #kb
TIME_STAMP_FORMAT = "[%Y-%m-%d %H:%M:%S]"

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

        # 클래스 이름을 알아내려면, frame의 locals에서 self를 찾아서 클래스명을 가져올 수 있음
        cls_name = None
        local_vars = frame.frame.f_locals
        if 'self' in local_vars:
            cls_name = type(local_vars['self']).__name__

        return cls_name, func_name, filename, lineno
        
    
    def info(self, message: str):
        cls_name, func_name, _, _ = self._get_caller_info()
        time_stamp = datetime.datetime.now().strftime(TIME_STAMP_FORMAT)
        caller = f"{cls_name}.{func_name}"
        log = f"[INFO]{time_stamp} {caller:30} {message}"
        self._logging(log)
        

    def _logging(self, log_message: str):
        # 로그파일 크기 확인
            # 이름 변경
        print(log_message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')



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



    
    

    
import datetime
import os
import inspect
import re

MAX_FILE_SIZE = 1 * 1024  # 10kb
TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


class Logger:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._init_file()
            self.initialized = True

    def _init_file(self):
        self.log_file = "latest.log"

        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'):
                pass

    def _get_caller_info(self) -> (str, str):
        stack = inspect.stack()
        if len(stack) < 3:
            return (None, None)

        frame = stack[2]
        frame_info = inspect.getframeinfo(frame[0])

        func_name = frame_info.function
        cls_name = None
        local_vars = frame.frame.f_locals
        if 'self' in local_vars:
            cls_name = type(local_vars['self']).__name__
        return cls_name, func_name

    def info(self, message: str):
        cls_name, func_name = self._get_caller_info()
        time_stamp = datetime.datetime.now().strftime(TIME_STAMP_FORMAT)
        caller = f"{cls_name}.{func_name}"
        log = f"[INFO][{time_stamp}] {caller:30} {message}"
        self._logging(log)

    def _logging(self, log_message: str):
        if self._check_log_file_size_max():
            self._change_log_file_name()
            self._compress_log_file()
        print(log_message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def _check_log_file_size_max(self) -> bool:
        if not os.path.exists(self.log_file):
            return False
        if os.path.getsize(self.log_file) > MAX_FILE_SIZE:
            return True
        return False

    def _change_log_file_name(self):
        last_log_time = self._get_last_log_time()
        os.rename(self.log_file, f"until_{last_log_time}.log")

    def _compress_log_file(self):
        for filename in os.listdir('.'):
            if filename.startswith('until') and filename.endswith('.log'):
                new_name = filename[:-4] + '.zip'  # .log → .zip
                os.rename(filename, new_name)

    def _get_last_log_time(self) -> str:
        with open(self.log_file, 'rb') as f:
            f.seek(-2, os.SEEK_END)  # 파일 끝에서 시작
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()

        match = re.search(r'([^]]*)?\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', last_line)
        dt = datetime.datetime.strptime(match.group(2), TIME_STAMP_FORMAT)
        last_log_time = dt.strftime("%Y%m%d_%Hh_%Mm_%Ss")
        return last_log_time


class AAA:
    def __init__(self):
        self.num = 1
        self.logger = Logger()

    def a(self):
        self.logger.info(f"aaa {self.num}")
        self.num += 1


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

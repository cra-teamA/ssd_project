import datetime
import os
import inspect
import re

MAX_FILE_SIZE = 10 * 1024  # 10kb
TIME_STAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FOLDER = os.path.join(os.path.abspath(__file__).split("shell")[0], "log")

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
        os.makedirs(LOG_FOLDER, exist_ok=True)
        os.chdir(LOG_FOLDER)

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

    def set_log(self, message: str):
        cls_name, func_name = self._get_caller_info()
        time_stamp = datetime.datetime.now().strftime(TIME_STAMP_FORMAT)
        caller = f"{cls_name}.{func_name}"
        log = f"[{time_stamp}] {caller:30} {message}"
        self._logging(log)

    def _logging(self, log_message: str):
        if self._check_log_file_size_max():
            self._compress_log_file()
            self._change_log_file_name()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')

    def _compress_log_file(self):
        for filename in os.listdir('.'):
            if filename.startswith('until') and filename.endswith('.log'):
                new_name = filename[:-4] + '.zip'
                os.rename(filename, new_name)

    def _check_log_file_size_max(self) -> bool:
        if not os.path.exists(self.log_file):
            return False
        if os.path.getsize(self.log_file) > MAX_FILE_SIZE:
            return True
        return False

    def _change_log_file_name(self):
        last_log_time = self._get_last_log_time()
        os.rename(self.log_file, f"until_{last_log_time}.log")

    def _get_last_log_time(self) -> str:
        with open(self.log_file, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()

        get_last_time = re.search(r'([^]]*)?\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', last_line).group(2)
        last_log_time = datetime.datetime.strptime(get_last_time, TIME_STAMP_FORMAT).strftime("%Y%m%d_%Hh_%Mm_%Ss")
        return last_log_time

class TestClass:
    def __init__(self):
        self.num = 100
        self.logger = Logger()

    def test(self):
        self.logger.set_log(f"loglog{self.num}")
        self.num -= 1


def main():
    import time
    tc = TestClass()
    for _ in range(30):
        tc.test()
        time.sleep(0.2)


if __name__ == "__main__":
    main()

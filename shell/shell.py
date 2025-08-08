import os
import subprocess
import sys
from abc import ABC

from shell.shell_command import FullRead, Help, Write, Exit, FullWrite, Erase, EraseRange, Flush

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logger import Logger
from shell_command import Read

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from scripts.ScriptRunner import ScriptRunner

MIN_LBA = 0
MAX_LBA = 99
MAX_VALUE_LENGTH = 10
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
SSD_COMMAND = os.path.join(PROJECT_ROOT, 'ssd.bat')


class Shell:
    def __init__(self):
        self.logger = Logger()

    def read(self, read_command: str, is_script: bool = False):
        _read = Read(read_command,is_script)
        _read.run()
        return _read.result
    def fullread(self, read_command: str):
        _full_read = FullRead(read_command)
        _full_read.run()
    def help(self, read_command: str):
        _help = Help(read_command)
        _help.run()
    def exit(self, read_command: str):
        _exit = Exit(read_command)
        _exit.run()
    def write(self, read_command: str, is_script: bool = False):
        _write = Write(read_command, is_script)
        _write.run()
    def fullwrite(self, read_command: str):
        _full_write = FullWrite(read_command)
        _full_write.run()
    def erase(self, read_command: str, is_script: bool = False):
        _erase = Erase(read_command,is_script)
        _erase.run()
    def erase_range(self, read_command: str, is_script: bool = False):
        _erase_range = EraseRange(read_command, is_script)
        _erase_range.run()
    def flush(self, command):
        _flush = Flush(command)
        _flush.run()

    def run_script(self, command):
        runner = ScriptRunner(self)
        runner.run(command)



def shell_command_mode(shell: Shell):
    COMMAND_MAP = {
        "read": shell.read,
        "write": shell.write,
        "fullread": shell.fullread,
        "fullwrite": shell.fullwrite,
        "erase": shell.erase,
        "erase_range": shell.erase_range,
        "flush": shell.flush,
        "help": shell.help,
        "exit": shell.exit,
    }
    while True:
        command = input("Shell > ").strip()
        if not command:
            continue
        cmd_name = command.split()[0]
        handler = COMMAND_MAP.get(cmd_name, shell.run_script)
        try:
            handler(command)
        except ValueError:
            print("INVALID COMMAND")


def main():
    shell = Shell()
    if len(sys.argv) == 1:
        shell_command_mode(shell)
    else:
        shell.run_script(f"{sys.argv[1]}")


if __name__ == "__main__":
    main()

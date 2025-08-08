import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logger import Logger
from shell_command import Command, FullRead, Help, Write, Exit, FullWrite, Erase, EraseRange, Flush, Read

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    
from scripts.ScriptRunner import ScriptRunner


COMMAND_MAP = {
        "read": Read,
        "write": Write,
        "fullread": FullRead,
        "fullwrite": FullWrite,
        "erase": Erase,
        "erase_range": EraseRange,
        "flush": Flush,
        "help": Help,
        "exit": Exit,
    }


class Shell:

    def __init__(self):
        self.logger = Logger()

    def run_script(self, command):
        runner = ScriptRunner()
        runner.run(command)



def shell_command_mode(shell: Shell):
    while True:
        command = input("Shell > ").strip()
        if not command:
            continue
        cmd_name = command.split()[0]
        handler = COMMAND_MAP.get(cmd_name, None)
        try:
            if handler is None:
                shell.run_script(command)
            else:
                cmd: Command = handler(command)
                cmd.run()
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

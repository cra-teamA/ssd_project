from pathlib import Path

from scripts.EraseAndWriteAging import EraseAndWriteAging
from scripts.FullWriteReadCompare import FullWriteReadCompare
from scripts.PartialLBAWrite import PartialLBAWrite
from scripts.WriteReadAging import WriteReadAging


class ScriptRunner:
    script_mapping = {
        "1": FullWriteReadCompare,
        "2": PartialLBAWrite,
        "3": WriteReadAging,
        "4": EraseAndWriteAging
    }

    def __init__(self):
        pass

    def is_valid_script_command(self, cmd: str) -> bool:
        if '_' not in cmd:
            return False
        idx, script_name = cmd.split('_', 1)
        return idx in self.script_mapping and script_name == self.script_mapping[idx].__name__

    def run(self, command: str):
        if ".txt" in command:
            self.run_script_file(command)
            return

        if not self.is_valid_script_command(command):
            print("INVALID COMMAMD")
            return

        script_class = self.script_mapping.get(command.split('_')[0])
        script = script_class()

        print("PASS" if script.run() else "FAIL")

    def run_script_file(self, script_filename):
        try:
            upper_dir = Path(__file__).resolve().parent.parent
            script_path = (upper_dir / script_filename).resolve()

            with open(script_path, "r", encoding="utf-8") as f:
                for line in f:
                    command = line.strip()
                    print(command, ' ___ ', "Run...", end='', flush=True)

                    if not self.is_valid_script_command(command):
                        print("INVALID COMMAMD")
                        return

                    script_class = self.script_mapping.get(command.split('_')[0])
                    script = script_class()

                    print("PASS" if script.run() else "FAIL!")


        except FileNotFoundError:
            print(f"[Error] Script file not found in upper directory: {script_filename}")
        except Exception as e:
            print(f"[Error] Failed to run script file: {e}")

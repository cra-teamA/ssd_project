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
        self.valid_script_names = []
        for script_idx, script_class in self.script_mapping.items():
            self.valid_script_names.append(script_idx + '_')
            self.valid_script_names.append(script_idx + '_' + script_class.__name__)

    def run(self, command: str):
        if ".txt" in command:
            self.run_script_file(command)
            return

        if command not in self.valid_script_names:
            print("INVALID COMMAMD")
            return

        script_class = self.script_mapping.get(command.split('_')[0])
        script = script_class()

        if script.run() :
            print("PASS")
        else:
            print("FAIL")
        return

    def run_script_file(self, script_filename):
        try:
            upper_dir = Path(__file__).resolve().parent.parent
            script_path = (upper_dir / script_filename).resolve()

            with open(script_path, "r", encoding="utf-8") as f:
                for line in f:
                    command = line.strip()
                    print(command, ' ___ ', "Run...", end='', flush=True)

                    if command not in self.valid_script_names:
                        print("INVALID COMMAMD")
                        return

                    script_class = self.script_mapping.get(command.split('_')[0])
                    script = script_class()

                    if script.run():
                        print("Pass")
                    else:
                        print("FAIL!")
                        return

        except FileNotFoundError:
            print(f"[Error] Script file not found in upper directory: {script_filename}")
        except Exception as e:
            print(f"[Error] Failed to run script file: {e}")

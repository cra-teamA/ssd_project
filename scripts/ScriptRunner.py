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

    def __init__(self, shell_instance):
        self.shell = shell_instance

    def parse_command(self, input_command: str):
        command = input_command.strip()
        if not command:
            return {"type": "empty"}

        if command.startswith("shell "):
            filename = command[6:].strip()
            return {"type": "shell", "filename": filename}

        parts = input_command.split("_", 1)
        if len(parts) != 2:
            return {"type": "invalid", "reason": "Format should be 'num_ClassName'"}

        num, class_name = parts
        script_class = self.script_mapping.get(num)

        if not script_class:
            return {"type": "invalid", "reason": f"Unknown script number: {num}"}

        if class_name != "" and class_name != script_class.__name__:
            return {"type": "invalid", "reason": f"Class name mismatch: {class_name} != {script_class.__name__}"}

        return {"type": "script", "num": num, "class_name": class_name, "script_class": script_class}

    def run(self, input_command: str):
        command = self.parse_command(input_command)

        if command['type'] == "invalid":
            print("INVALID COMMAND")
            return
        elif command["type"] == "shell":
            self.run_script_file(command['filename'])
            return

        script_class = self.script_mapping.get(command["num"])
        script = script_class(self.shell)

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

                    parsing_command = self.parse_command(command)
                    print(command, ' ___ ', "Run...", end='', flush=True)

                    if parsing_command['type'] == "invalid":
                        print(f"FAIL!({command} is INVALID COMMAND)")
                        return

                    script_class = self.script_mapping.get(parsing_command["num"])
                    script = script_class(self.shell)

                    if script.run():
                        print("Pass")
                    else:
                        print("FAIL!")
                        return

        except FileNotFoundError:
            print(f"[Error] Script file not found in upper directory: {script_filename}")
        except Exception as e:
            print(f"[Error] Failed to run script file: {e}")

from scripts.FullWriteReadCompare import FullWriteReadCompare
from scripts.PartialLBAWrite import PartialLBAWrite
from scripts.WriteReadAging import WriteReadAging

class ScriptRunner:

    script_mapping = {
        "1": FullWriteReadCompare,
        "2": PartialLBAWrite,
        "3": WriteReadAging,
    }

    def __init__(self, shell_instance):
        self.shell = shell_instance

    def run(self, command: str) -> bool | None:

        if not (parts := command.split("_", 1)) or len(parts) != 2:
            return None

        script_class = self.script_mapping.get(parts[0])
        if not script_class:
            return None

        script = script_class(self.shell)

        return script.run()

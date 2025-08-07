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

    def run(self, command: str) -> bool | None:

        if not (command_split := command.split("_", 1)) or len(command_split) != 2:
            return None

        num, class_name = command_split[0], command_split[1]

        script_class = self.script_mapping.get(num)
        if (not script_class) or \
                (class_name != "" and class_name != script_class.__name__):
            return None

        script = script_class(self.shell)
        return script.run()

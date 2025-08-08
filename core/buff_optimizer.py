from core.command import Command, command_factory, DEFAULT_VALUE

MAX_ERASE_SIZE = 10


class Optimizer:
    def __init__(self):
        ...

    def generate_new_commands(self, cache: dict) -> list[Command]:
        new_commands = []
        command = None
        for addr, val in sorted(cache.items()):
            if val == DEFAULT_VALUE:
                if not command:
                    command = command_factory('E', addr, 1)
                elif command.mode == 'E' and addr == command.lba + command.size:
                    command.size += 1
                    if command.size >= MAX_ERASE_SIZE:
                        new_commands.append(command)
                        command = None
                elif command.size or addr != command.lba + command.size:
                    new_commands.append(command)
                    command = command_factory('E', addr, 1)
            else:
                if command:
                    new_commands.append(command)
                command = command_factory('W', addr, val)
        if command:
            new_commands.append(command)
        return new_commands

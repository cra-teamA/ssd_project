import os

from core.command import Command, command_factory

MAX_BUFFER_SIZE = 5

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BUFFER_DIR = os.path.join(PROJECT_ROOT, 'buffer')

class CommandBuffer:

    def __init__(self):
        self.command_buffer=[]
        filenames = self._readDirectory()
        self.syncToList(filenames)
        self.syncToDirectory()

    def is_full(self) -> int:
        return len(self.command_buffer) >= MAX_BUFFER_SIZE

    def get(self)->list:
        return self.command_buffer

    def add(self, command :Command):
        self.command_buffer.append(command)
        return

    def truncate(self):
        self.command_buffer = []
        self.syncToDirectory()

    def print(self, prefix=''):
        for i, cmd in enumerate(self.command_buffer):
            if cmd is not None:
                print(f"{prefix}buffer[{i}] : {cmd.mode}, {cmd.lba}, {cmd.size}, {cmd.value}")
        return

    def replace(self, new_buffer):
        self.command_buffer = new_buffer

    def syncToDirectory(self):
        self._is_buffer_directory_valid()
        self._remove_file(BUFFER_DIR)
        self._create_file()
        self._create_empty_file()

    def syncToList(self, filenames):
        files = self._fill_empty_files(filenames)
        for filename in files:
            command = self._make_command_from_filename(filename)
            if command:
                self.add(command)

    def _readDirectory(self) -> list[str]:
        self._is_buffer_directory_valid()

        filenames = sorted(
            [f for f in os.listdir(BUFFER_DIR) if os.path.isfile(os.path.join(BUFFER_DIR, f))]
        )
        return filenames

    def _create_empty_file(self):
        current_size = len(self.command_buffer)
        for i in range(current_size, MAX_BUFFER_SIZE):
            filename = os.path.join(BUFFER_DIR, f"{i}_empty.txt")
            with open(filename, "w") as f:
                pass

    def _create_file(self):
        for i, cmd in enumerate(self.command_buffer):
            idx = i
            command = cmd.mode
            lba = cmd.lba
            value = cmd.value
            size = cmd.size

            if command == 'W':  # 1_W_0_0x00000000.txt
                filename = f"{idx}_{command}_{lba}_{value}.txt"
            elif command == 'E':  # 2_E_3_5.txt
                filename = f"{idx}_{command}_{lba}_{size}.txt"
            else:
                continue  # 기타 명령은 건너뜀

            filename = os.path.join(BUFFER_DIR, filename)
            with open(filename, "w") as f:
                pass

    def _remove_file(self, file_directory):
        for filename in os.listdir(file_directory):
            file_path = os.path.join(file_directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def _is_buffer_directory_valid(self):
        if not os.path.exists(BUFFER_DIR):
            os.makedirs(BUFFER_DIR, exist_ok=True)

    def _fill_empty_files(self, filenames):
        result = filenames.copy()
        while len(result) < MAX_BUFFER_SIZE:
            result.append("")
        return result[:MAX_BUFFER_SIZE]

    def _make_command_from_filename(self, filename):
        name = filename.rsplit('.', 1)[0]
        if not name:
            return None
        parts = name.split('_')
        if len(parts) < 4:
            return None
        return command_factory(parts[1], int(parts[2]), parts[3])

buffer = CommandBuffer()

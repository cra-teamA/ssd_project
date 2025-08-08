import os

from core.command import Command, command_factory

MAX_BUFFER_SIZE = 5

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BUFFER_DIR = os.path.join(PROJECT_ROOT, 'buffer')

class CommandBuffer:

    def __init__(self):
        self.command_buffer=[]
        filenames = self.readDirectory()
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


    def readDirectory(self) -> list[str]:
        self.is_buffer_directory_valid()

        filenames = sorted(
            [f for f in os.listdir(BUFFER_DIR) if os.path.isfile(os.path.join(BUFFER_DIR, f))]
        )
        return filenames


    def syncToList(self , filenames):
        while len(filenames) < MAX_BUFFER_SIZE:
            filenames.append("")
        filenames = filenames[:MAX_BUFFER_SIZE]
        file = filenames.copy()

        for i in range(len(filenames)):
            file[i] = file[i].rsplit('.', 1)[0]
            if file[i] == '':
                continue

            parts = file[i].split('_')
            if len(parts) < 4:
                continue

            self.add(command_factory(parts[1], int(parts[2]), parts[3]))


    def syncToDirectory(self):
        self.is_buffer_directory_valid()
        self.remove_file(BUFFER_DIR)
        self.create_file()
        self.create_empty_file()

    def create_empty_file(self):
        current_size = len(self.command_buffer)
        for i in range(current_size, MAX_BUFFER_SIZE):
            filename = os.path.join(BUFFER_DIR, f"{i}_empty.txt")
            with open(filename, "w") as f:
                pass

    def create_file(self):
        for i, cmd in enumerate(self.command_buffer):
            idx = i
            command = cmd.mode
            lba = cmd.lba
            value = cmd.value
            size = cmd.size

            # 파일명 생성
            if command == 'W':  # 1_W_0_0x00000000.txt
                filename = f"{idx}_{command}_{lba}_{value}.txt"
            elif command == 'E':  # 2_E_3_5.txt
                filename = f"{idx}_{command}_{lba}_{size}.txt"
            else:
                continue  # 기타 명령은 건너뜀

            # 실제 파일 생성
            filename = os.path.join(BUFFER_DIR, filename)
            with open(filename, "w") as f:
                pass

    def remove_file(self,file_directory):
        for filename in os.listdir(file_directory):
            file_path = os.path.join(file_directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def replace(self, new_buffer):
        self.command_buffer = new_buffer

    def is_buffer_directory_valid(self):
        if not os.path.exists(BUFFER_DIR):
            os.makedirs(BUFFER_DIR, exist_ok=True)

buffer = CommandBuffer()

import os
from dataclasses import dataclass

from core.command import Command, command_factory

MAX_BUFFER_SIZE = 5

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BUFFER_DIR = os.path.join(PROJECT_ROOT, 'buffer')

class CommandBuffer:

    def __init__(self):
        self.command_buffer=[]
        #buffer 디렉토리내 파일 읽기
        filenames = self.readDirectory()

        #읽은 파일들을 buffer로 동기화
        self.syncToList(filenames)

    def is_full(self):
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
        if not os.path.exists(BUFFER_DIR):
            os.makedirs(BUFFER_DIR, exist_ok=True)

        filenames = [f for f in os.listdir(BUFFER_DIR) if os.path.isfile(os.path.join(BUFFER_DIR, f))]
        sorted_files = sorted(filenames)
        return sorted_files


    def syncToList(self , filenames):
        while len(filenames) < MAX_BUFFER_SIZE:
            filenames.append("")
        filenames = filenames[:MAX_BUFFER_SIZE]
        file = filenames.copy()

        for i in range(MAX_BUFFER_SIZE):
            file[i] = file[i].rsplit('.', 1)[0]
            if file[i] == '':
                continue

            parts = file[i].split('_')
            idx = int(parts[0])
            cmd = parts[1]
            lba = int(parts[2])
            param = parts[3]


            self.command_buffer.append(command_factory(cmd,lba,param))

    def syncToDirectory(self):
        #buffer 내 파일 전체 삭제
        if not os.path.exists(BUFFER_DIR):
            os.makedirs(BUFFER_DIR, exist_ok=True)

        for filename in os.listdir(BUFFER_DIR):
            file_path = os.path.join(BUFFER_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


        for i, cmd in enumerate(self.command_buffer):
            idx = i
            command = cmd.mode
            lba = cmd.lba
            value = cmd.value
            size = cmd.size

            # 파일명 생성
            if command == 'W':  # 1_W_0_0x00000000.txt

                filename = f"{idx}_{command}_{lba}_{value}.txt"
            elif command == 'E':    # 2_E_3_5.txt

                filename = f"{idx}_{command}_{lba}_{size}.txt"
            else:
                continue  # 기타 명령은 건너뜀

            # 실제 파일 생성
            filename = os.path.join(BUFFER_DIR, filename)
            with open(filename, "w") as f:
                pass

    def replace(self, new_buffer):
        self.command_buffer = new_buffer


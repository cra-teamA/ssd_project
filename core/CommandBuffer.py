import os
from dataclasses import dataclass

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BUFFER_DIR = os.path.join(PROJECT_ROOT, 'buffer')

@dataclass
class Command:
    command: str
    lba: int
    size: int
    value: str = None  # 기본값 None

class CommandBuffer:
    command_buffer: list[Command]

    def __init__(self):
        self.command_buffer = [Command(None,None,None,None) for _ in range(6)]

        #buffer 디렉토리내 파일 읽기
        filenames = self.readDirectory()

        #읽은 파일들을 buffer로 동기화
        self.syncToList(filenames)

    #Command Buffer List를 get하는 메소드
    def get(self)->list[Command]:
        return self.command_buffer
    #Command Buffer에 command를 추가하는 메소드
    def add(self, command :Command):
        return
    #현재 존재하는 command들을 모두 지우는 메소드
    def truncate(self):
        return
    #command Buffer에 있는 command들을 모두 nand.txt에 반영하는 메소드
    def flush(self):
        return

    #Directory를 읽어서 파일명을 확인하는 메소드
    def readDirectory(self) -> list[str]:
        filenames = [f for f in os.listdir(BUFFER_DIR) if os.path.isfile(os.path.join(BUFFER_DIR, f))]
        #print(f"ReadDirectory : {filenames}")
        return filenames

    #읽은 파일명을 command_buffer list에 동기화하는 메소드
    def syncToList(self , filenames):
        while len(filenames) < 5:
            filenames.append("")
        filenames = filenames[:5]
        file = filenames.copy()

        for i in range(5):
            file[i] = file[i].rsplit('.', 1)[0]
            if file[i] == '':
                continue

            parts = file[i].split('_')
            idx = int(parts[0])
            self.command_buffer[idx].command = parts[1]

            if parts[1] == 'W': #1_W_0_0x00000000.txt
                self.command_buffer[idx].lba = int(parts[2])
                self.command_buffer[idx].size = None
                self.command_buffer[idx].value = parts[3]

            if parts[1] == 'E': #2_E_3_5.txt
                self.command_buffer[idx].lba = parts[2]
                self.command_buffer[idx].size = parts[3]
                self.command_buffer[idx].value = None

            #print(f"SyncToList : {self.command_buffer[i].command} , {self.command_buffer[i].lba} , {self.command_buffer[i].size} , {self.command_buffer[i].value}")

    #command_buffer의 내용을 파일로 동기화하는 메소드
    def syncToDirectory(self):
        #buffer 내 파일 전체 삭제
        for filename in os.listdir(BUFFER_DIR):
            file_path = os.path.join(BUFFER_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("syncToDirectory")
        self.command_buffer[0].command = "W"
        self.command_buffer[0].lba = 2
        self.command_buffer[0].value = "0x00000000"

        self.command_buffer[1].command = "E"
        self.command_buffer[0].lba = 3
        self.command_buffer[0].size = 5

        #파일명 추출
        for i, cmd in enumerate(self.command_buffer):
            idx = i
            command = cmd.command
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

            #print(filename)
            # 실제 파일 생성
            filename = os.path.join(BUFFER_DIR, filename)
            with open(filename, "w") as f:
                pass







from ssd_controller import SSDController
import json
import os

# 현재 테스트 파일 위치 기준으로 루트 디렉토리 계산
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SSD_NAND_PATH = os.path.join(PROJECT_ROOT, 'ssd_nand.txt')
SSD_OUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
SINGLE_TEST_DATA = {1:"0xaaaaaaaa"}
def test_read():
    print(PROJECT_ROOT)
    controller = SSDController()
    with open(SSD_NAND_PATH, "w", encoding="utf-8") as f:
        json.dump(SINGLE_TEST_DATA, f, ensure_ascii=False)
    controller.read(1)
    with open(SSD_OUT_PATH, "r", encoding="utf-8") as f:
        actual = f.read()
    assert actual == SINGLE_TEST_DATA.get(1)
import pytest

from ssd_controller import SSDController
import json
import os

# 현재 테스트 파일 위치 기준으로 루트 디렉토리 계산
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(PROJECT_ROOT)
print(PROJECT_ROOT)
print(PROJECT_ROOT)
SSD_NAND_PATH = os.path.join(PROJECT_ROOT, 'ssd_nand.txt')
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
SINGLE_TEST_DATA = {1:"0xaaaaaaaa"}
ERROR = 'ERROR'

@pytest.fixture
def controller_with_single_data():
    controller = SSDController()
    with open(SSD_NAND_PATH, "w", encoding="utf-8") as f:
        json.dump(SINGLE_TEST_DATA, f, ensure_ascii=False)
    return controller

def get_ssd_output():
    with open(SSD_OUTPUT_PATH, "r", encoding="utf-8") as f:
        actual = f.read()
    return actual

def test_read(controller_with_single_data):
    controller_with_single_data.read(1)
    assert get_ssd_output() == SINGLE_TEST_DATA.get(1)

def test_read_invalid_minus_lba(controller_with_single_data):
    controller_with_single_data.read(-1)
    assert get_ssd_output() == ERROR

def test_read_invalid_hundred_lba(controller_with_single_data):
    controller_with_single_data.read(100)
    assert get_ssd_output() == ERROR

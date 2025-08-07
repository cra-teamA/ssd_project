import pytest
from core.ssd_controller import SSDController
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
ERROR = 'ERROR'


def test_erase_success():
    ssd = SSDController()
    assert ssd.erase(1, 10) == True
    assert ssd.erase(0, 10) == True
    assert ssd.erase(99, 10) == True

def test_erase_invalid_size_fail():
    ssd = SSDController()
    assert ssd.erase(0, 11) == False

def test_erase_invalid_addr_fail():
    ssd = SSDController()
    assert ssd.erase(-1, 1) == False
    assert ssd.erase(100, 1) == False

import pytest
from core.ssd_controller import SSDController
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
ERROR = 'ERROR'


def test_create_ssd_controller_instance():
    ssd = SSDController()
    assert isinstance(ssd, SSDController)


def test_write_valid_addr():
    ssd = SSDController()
    assert ssd.write(0, '0x10000000') == True


@pytest.mark.parametrize("invalid_addr", [100, -1, '100', None])
def test_write_invalid_addr(invalid_addr):
    ssd = SSDController()
    assert ssd.write(invalid_addr, '0x100') == False


@pytest.mark.parametrize("valid_val", ['0x0fffff01', '0X00000000', '0xf000000f', '0xFfFAFAAA'])
def test_write_valid_val(valid_val):
    ssd = SSDController()
    assert ssd.write(0, valid_val) == True


@pytest.mark.parametrize("invalid_val", [100, -1, '100', None, '00', 'aa1', '0xkk',
                                         '0x11111111111111111'])
def test_write_invalid_val(invalid_val):
    ssd = SSDController()
    assert ssd.write(0, invalid_val) == False


def get_ssd_output():
    with open(SSD_OUTPUT_PATH, "r", encoding="utf-8") as f:
        actual = f.read()
    return actual


@pytest.mark.parametrize("addr, val", [(99, '0x10000000'), (10, '0x10f0000f')])
def test_write_right_written(addr, val):
    ssd = SSDController()
    ssd.write(addr, val)
    ssd.read(addr)
    assert get_ssd_output() == val


@pytest.mark.parametrize("invalid_val", [100, -1, '100', None, '00', 'aa1', '0xkk',
                                         '0x11111111111111111'])
def test_write_check_output_file_when_invalid_input(invalid_val):
    ssd = SSDController()
    ssd.write(0, invalid_val)
    assert get_ssd_output() == ERROR

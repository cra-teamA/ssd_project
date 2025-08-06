import pytest
from ssd_controller import SSDController


def test_create_ssd_controller_instance():
    ssd = SSDController()
    assert isinstance(ssd, SSDController)


def test_write_valid_addr():
    ssd = SSDController()
    assert ssd.write(0, '0x100') == True


@pytest.mark.parametrize("invalid_addr", [100, -1, '100', None])
def test_write_invalid_addr(invalid_addr):
    ssd = SSDController()
    assert ssd.write(invalid_addr, '0x100') == False


@pytest.mark.parametrize("valid_val", ['0x001', '0X001', '0xff', '0xFf'])
def test_write_valid_val(valid_val):
    ssd = SSDController()
    assert ssd.write(0, valid_val) == True


@pytest.mark.parametrize("invalid_val", [100, -1, '100', None, '00', 'aa1', '0xkk',
                                         '0x11111111111111111'])
def test_write_invalid_val(invalid_val):
    ssd = SSDController()
    assert ssd.write(0, invalid_val) == False


@pytest.mark.parametrize("addr, val", [(99, '0x100'), (10, '0x10ff')])
def test_write_right_written(addr, val):
    ssd = SSDController()
    ssd.write(addr, val)
    assert ssd._temp_read_for_test(addr) == val


@pytest.mark.parametrize("addr, val", [(99, '0x100'), (10, '0x10ff')])
def test_write_right_written(addr, val):
    ssd = SSDController()
    ssd.write(addr, val)
    assert ssd._temp_read_for_test(addr) == val


@pytest.mark.parametrize("invalid_val", [100, -1, '100', None, '00', 'aa1', '0xkk',
                                         '0x11111111111111111'])
def test_write_check_output_file_when_invalid_input(invalid_val):
    ssd = SSDController()
    ssd.write(0, invalid_val)
    assert ssd.check_output_msg() == 'ERROR'

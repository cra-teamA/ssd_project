import pytest
from ssd_controller import SSDController


def test_create_ssd_controller_instance():
    ssd = SSDController()
    assert isinstance(ssd, SSDController)


def test_write_addr():
    ssd = SSDController()
    assert ssd.write(0, '0x100') == True



@pytest.mark.parametrize("invalid_addr", [100, -1, '100', None])
def test_write_invalid_addr(invalid_addr):
    ssd = SSDController()
    assert ssd.write(invalid_addr, '0x100') == False


def test_write_valid_val():
    ssd = SSDController()
    assert ssd.write(0, '0x001') == True
    assert ssd.write(0, '0X001') == True

@pytest.mark.parametrize("invalid_val", [100, -1, '100', None, '00', 'aa1', '0xkk',
                                         '0x11111111111111111'])
def test_write_invalid_val(invalid_val):
    ssd = SSDController()
    assert ssd.write(0, invalid_val) == False

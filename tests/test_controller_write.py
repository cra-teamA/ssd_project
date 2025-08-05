import pytest
from ssd_controller import SSDController


def test_create_ssd_controller_instance():
    ssd = SSDController()
    assert isinstance(ssd, SSDController)


def test_write_addr():
    ssd = SSDController()
    assert ssd.write(0, '0X100') == True


@pytest.mark.parametrize("invalid_input", [100, -1, '100', None])
def test_write_invalid_addr(invalid_input):
    ssd = SSDController()
    assert ssd.write(invalid_input, '0X100') == False

def test_write_invalid_val():
    ssd = SSDController()
    assert ssd.write(0, 100) == False


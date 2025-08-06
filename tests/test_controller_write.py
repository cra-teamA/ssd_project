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

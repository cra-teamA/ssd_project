import pytest
from ssd_controller import SSDController


def test_create_ssd_controller_instance():
    ssd = SSDController()
    assert isinstance(ssd, SSDController)


def test_write_addr():
    ssd = SSDController()
    return ssd.write(0, '100') == True

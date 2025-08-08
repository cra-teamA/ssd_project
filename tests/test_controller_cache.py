import pytest
from pytest_mock import mocker
from core.ssd_controller import SSDController
from core.command import command_factory, DEFAULT_VALUE


@pytest.fixture
def successs_buffer():
    buffer = [
        command_factory("W", 0, "0xAAAABBBB"),
        command_factory("W", 1, "0xCCCCDDDD"),
        command_factory("E", 2, 10),
        command_factory("W", 3, "0x12345678"),
        command_factory("E", 4, 1),
        command_factory("W", 5, "0xDEADBEEF")
    ]
    cache = {0: '0xAAAABBBB',
             1: '0xCCCCDDDD',
             2: '0x00000000',
             3: '0x12345678',
             4: '0x00000000',
             5: '0xDEADBEEF',
             6: '0x00000000',
             7: '0x00000000',
             8: '0x00000000',
             9: '0x00000000',
             10: '0x00000000',
             11: '0x00000000'}
    return buffer, cache


def test_update_cache_success(successs_buffer):
    buffer, expected_cache = successs_buffer
    ssd = SSDController()
    ssd.init_cache(buffer)
    assert ssd.cache == expected_cache

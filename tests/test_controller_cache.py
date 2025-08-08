import pytest
from pytest_mock import mocker
from core.ssd_controller import SSDController
from core.command import command_factory, DEFAULT_VALUE


@pytest.fixture
def successs_buffer():
    buffer = [
        command_factory("W", 0, "0xaaaabbbb"),
        command_factory("W", 1, "0xccccdddd"),
        command_factory("E", 2, 10),
        command_factory("W", 3, "0x12345678"),
        command_factory("E", 4, 1),
        command_factory("W", 5, "0xdeadbeef")
    ]
    cache = {0: '0xaaaabbbb',
             1: '0xccccdddd',
             2: '0x00000000',
             3: '0x12345678',
             4: '0x00000000',
             5: '0xdeadbeef',
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

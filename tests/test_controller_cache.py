import pytest
from pytest_mock import mocker
from core.ssd_controller import SSDController
from core.command import Command, DEFAULT_VALUE


@pytest.fixture
def successs_buffer():
    buffer = [
        Command("W", 0, "0xAAAABBBB"),
        Command("W", 1, "0xCCCCDDDD"),
        Command("E", 2, 10),
        Command("W", 3, "0x12345678"),
        Command("E", 4, 1),
        Command("W", 5, "0xDEADBEEF")
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

    assert ssd.update_cache(buffer) == expected_cache

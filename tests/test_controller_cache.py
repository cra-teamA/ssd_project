import pytest
from pytest_mock import mocker
from core.ssd_controller import SSDController


@pytest.fixture
def successs_buffer():
    return [
        {"command": "W", "lba": 0, "size": None, "value": "0xAAAABBBB"},
        {"command": "W", "lba": 1, "size": None, "value": "0xCCCCDDDD"},
        {"command": "E", "lba": 2, "size": 10, "value": None},
        {"command": "W", "lba": 3, "size": None, "value": "0x12345678"},
        {"command": "E", "lba": 4, "size": 1, "value": None},
        {"command": "W", "lba": 5, "size": None, "value": "0xDEADBEEF"},
    ],{0: '0xAAAABBBB',
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

def test_update_cache_success(successs_buffer):
    buffer, expected_cache = successs_buffer
    ssd = SSDController()

    assert ssd.update_cache(buffer) == expected_cache
import pytest
from unittest.mock import patch

from core.command_buffer import CommandBuffer


def test_init_command_buffer():
    buffer = CommandBuffer()
    assert buffer is not None

def test_init_calls_method(monkeypatch):
    # readDirectory, syncToList를 patch해서 호출여부 확인
    with patch.object(CommandBuffer, "readDirectory", return_value=['0_W_1_0x44442222.txt', '1_E_25_10.txt']) as mock_read, \
            patch.object(CommandBuffer, "syncToList") as mock_sync:
        buffer = CommandBuffer()
        # 두 메소드가 생성자에서 호출됐는지 확인
        assert mock_read.called, "readDirectory가 호출되지 않음"
        assert mock_sync.called, "syncToList가 호출되지 않음"
        mock_read.assert_called_once_with()
        mock_sync.assert_called_once_with(['0_W_1_0x44442222.txt', '1_E_25_10.txt'])




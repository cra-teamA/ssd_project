import os

import pytest
from unittest.mock import patch

from core.command import command_factory
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


def test_truncate():
    buf = CommandBuffer()
    buf.add(command_factory('W', 2, '0xabcdef'))
    assert len(buf.get()) > 0
    buf.truncate()
    assert buf.get() == []


def test_is_full():
    buf = CommandBuffer()
    buf.truncate()
    from core.command import Command
    for i in range(5):
        buf.add(command_factory('W', i, f'0x{i:08x}'))
    assert buf.is_full() is True

def test_print_output(capsys):
    buf = CommandBuffer()
    buf.truncate()
    buf.add(command_factory('W', 1, '0x11111111'))
    buf.print('TEST_')
    captured = capsys.readouterr()
    assert "TEST_buffer[0]" in captured.out or "TEST_buffer[0]:" in captured.out


def test_sync_to_directory(tmp_path):
    from core.command import Command
    # BUFFER_DIR 임시로 바꾸기
    import core.command_buffer
    orig_buffer_dir = core.command_buffer.BUFFER_DIR
    core.command_buffer.BUFFER_DIR = str(tmp_path)
    buf = CommandBuffer()
    buf.truncate()
    buf.add(command_factory('W', 0, '0x11111111'))
    buf.add(command_factory('E', 1, 10))
    buf.syncToDirectory()
    files = os.listdir(str(tmp_path))
    assert any(f.endswith("_empty.txt") for f in files)
    assert any(f.startswith("0_W") for f in files)
    core.command_buffer.BUFFER_DIR = orig_buffer_dir  # 원복

def test_replace_buffer():
    from core.command import Command
    buf = CommandBuffer()
    new_buf = [command_factory('W', 1, '0x22222222')]
    buf.replace(new_buf)
    assert buf.command_buffer == new_buf
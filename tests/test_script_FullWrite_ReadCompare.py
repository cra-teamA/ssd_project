import pytest
from unittest.mock import Mock
from scripts.FullWriteReadCompare import FullWriteReadCompare
from shell.shell import Shell
from scripts.BaseScript import BaseScript


@pytest.fixture
def mock_dummy_shell_interface():
    mock = Mock(spec=Shell)
    return mock

@pytest.fixture
def mock_normal_shell_interface():
    mock = Mock(spec=Shell)
    def read_side_effect(cmd, isCommandFromScript):  # 인자 2개
        lba = int(cmd.split()[1])
        group = lba // 5
        return f"0x{group:08x}"
    mock.read.side_effect = read_side_effect
    return mock


@pytest.fixture
def mock_compare_fail_shell_interface():
    mock = Mock(spec=Shell)
    def read_side_effect(cmd, isCommandFromScript):  # ← 인자 2개
        lba = int(cmd.split()[1])
        if lba == 12:
            return "0x00000007"
        group = lba // 5
        return f"0x{group:08x}"
    mock.read.side_effect = read_side_effect
    return mock

def test_script_init(mock_dummy_shell_interface):
    script = FullWriteReadCompare()
    assert script is not None

def test_script_run_pass(mocker):
    fake_memory = {}

    def fake_read(self, lba):
        return fake_memory.get(lba, '0x00000000')

    def fake_write(self, lba, data):
        fake_memory[lba] = data

    mocker.patch.object(BaseScript, 'read_lba', fake_read)
    mocker.patch.object(BaseScript, 'write_lba', fake_write)

    script = FullWriteReadCompare()
    result = script.run()

    assert result is True


def test_script_run_fail(mocker):
    fake_memory = {}
    def fake_read(self, lba):
        if lba == 12:
            if lba == 12:
                return "0x00000007"
        return fake_memory.get(lba, '0x00000000')

    def fake_write(self, lba, data):
        fake_memory[lba] = data

    mocker.patch.object(BaseScript, 'read_lba', fake_read)
    mocker.patch.object(BaseScript, 'write_lba', fake_write)

    script = FullWriteReadCompare()
    result = script.run()

    assert result is False
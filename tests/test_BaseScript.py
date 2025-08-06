import pytest
from scripts.BaseScript import BaseScript
from shell.shell import Shell

class DummyScript(BaseScript):
    def run(self):
        pass  # run 추상 메서드 구현

def test_base_script_can_be_instantiated(mocker):
    mock_shell = mocker.Mock(spec=Shell)
    instance = DummyScript(mock_shell)
    assert isinstance(instance, BaseScript)

def test_write_lba_calls_shell_write(mocker):
    data = 0xAB
    lba = 0x10

    mock_shell = mocker.Mock()
    mock_shell.read.return_value = data
    script = DummyScript(mock_shell)

    script.write_lba(lba, data)
    result = script.read_lba(lba)

    # then
    assert result == data
    mock_shell.write.assert_called_once_with(lba, data)
    mock_shell.write.assert_called_once_with(lba, data)
    mock_shell.read.assert_called_once_with(lba)

def test_read_lba_calls_shell_read_and_returns_value(mocker):
    mock_shell = mocker.Mock(spec=Shell)
    mock_shell.read.return_value = 0xCD

    script = DummyScript(mock_shell)

    result = script.read_lba(0x20)

    mock_shell.read.assert_called_once_with(0x20)
    assert result == 0xCD
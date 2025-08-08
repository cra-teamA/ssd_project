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
    mock_shell = mocker.Mock(spec=Shell)
    script = DummyScript(mock_shell)

    script.write_lba("3", "0xABCDEF12")

    mock_shell.write.assert_called_once_with("write 3 0xABCDEF12", True)


def test_read_lba_calls_shell_read_and_returns_value(mocker):
    mock_shell = mocker.Mock(spec=Shell)
    mock_shell.read.return_value = "0x12345678"
    script = DummyScript(mock_shell)

    result = script.read_lba("3")

    mock_shell.read.assert_called_once_with('read 3', True)
    assert result == "0x12345678"

import pytest
from scripts.BaseScript import BaseScript
from shell.shell_command import Read

class DummyScript(BaseScript):
    def run(self):
        pass  # run 추상 메서드 구현

def test_base_script_can_be_instantiated(mocker):
    instance = DummyScript()
    assert isinstance(instance, BaseScript)

def test_write_lba_calls_shell_write(mocker):
    mock_write = mocker.patch("shell.shell_command.Write.run")
    script = DummyScript()
    script.write_lba("3", "0xABCDEF12")
    mock_write.assert_called_once()

def test_read_lba_calls_shell_read_and_returns_value(mocker):
    def fake_run(self):
        self.result = "0x12345678"
    mocker.patch.object(Read, 'run', fake_run)
    script = DummyScript()
    result = script.read_lba("3")
    assert result == "0x12345678"





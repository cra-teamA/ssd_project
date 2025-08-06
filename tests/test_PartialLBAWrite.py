import pytest
from scripts.PartialLBAWrite import PartialLBAWrite
from shell.shell import Shell


def test_partial_lba_write_class_can_be_instantiated(mocker):
    mock_shell = mocker.Mock(spec=Shell)
    instance = PartialLBAWrite('test_interface')
    assert isinstance(instance, PartialLBAWrite)

def test_partial_lba_write_passes(mocker):
    mock_shell = mocker.Mock(spec=Shell)

    fake_memory = {}

    def fake_write(lba, data):
        fake_memory[lba] = data

    def fake_read(lba):
        return fake_memory.get(lba, 0)

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read

    script = PartialLBAWrite(mock_shell)
    result = script.run()

    assert result is True

def test_partial_lba_write_fails_on_mismatch(mocker):
    mock_shell = mocker.Mock(spec=Shell)

    def fake_write(lba, data):
        pass  # write 무시

    def fake_read(lba):
        return -1  # 항상 잘못된 값

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read

    script = PartialLBAWrite(mock_shell)
    result = script.run()

    assert result is False
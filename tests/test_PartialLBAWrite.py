import pytest
from scripts.PartialLBAWrite import PartialLBAWrite
from shell.shell import Shell


def test_partial_lba_write_class_can_be_instantiated(mocker):
    mock_shell = mocker.Mock(spec=Shell)
    instance = PartialLBAWrite(mock_shell)
    assert isinstance(instance, PartialLBAWrite)


def test_partial_lba_write_passes(mocker):
    mock_shell = mocker.Mock(spec=Shell)

    fake_memory = {}

    def fake_write(cmd, isCommandFromScript):
        _, lba, data = cmd.split()
        fake_memory[lba] = data

    def fake_read(cmd, isCommandFromScript):
        _, lba = cmd.split()
        return fake_memory.get(lba, -1)

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read

    script = PartialLBAWrite(mock_shell)
    result = script.run()

    assert result is True


def test_partial_lba_write_fails_on_mismatch(mocker):
    mock_shell = mocker.Mock(spec=Shell)

    def fake_write(cmd, isCommandFromScript):
        pass  # write 무시

    def fake_read(cmd, isCommandFromScript):
        return -1  # 항상 잘못된 값

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read

    script = PartialLBAWrite(mock_shell)
    result = script.run()

    assert result is False

import pytest
from scripts.WriteReadAging import WriteReadAging
from shell.shell import Shell


def test_partial_lba_write_class_can_be_instantiated(mocker):
    mock_shell = mocker.Mock(spec=Shell)
    instance = WriteReadAging(mock_shell)
    assert isinstance(instance, WriteReadAging)

def test_write_read_aging_succeeds(mocker):
    mock_shell = mocker.Mock(spec=Shell)

    # LBA마다 읽은 값이 항상 쓰인 값과 같도록 설정
    fake_memory = {}

    def fake_write(cmd, isCommandFromScript):
        _, lba, data = cmd.split()
        fake_memory[lba] = data

    def fake_read(cmd, isCommandFromScript):
        _, lba = cmd.split()
        return fake_memory.get(lba, -1)

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read

    script = WriteReadAging(mock_shell)
    result = script.run()

    assert result is True

def test_write_read_aging_fails_when_data_mismatch(mocker):
    mock_shell = mocker.Mock(spec=Shell)

    def fake_write(cmd, isCommandFromScript):
        pass  # write 무시

    def fake_read(cmd, isCommandFromScript):
        return -1  # 항상 잘못된 값

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read

    script = WriteReadAging(mock_shell)
    result = script.run()

    assert result is False
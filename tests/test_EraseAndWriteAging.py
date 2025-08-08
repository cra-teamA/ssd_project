import pytest
from scripts.EraseAndWriteAging import EraseAndWriteAging
from shell.shell import Shell


def test_erase_and_write_aging_class_can_be_instantiated(mocker):
    mock_shell = mocker.Mock(spec=Shell)
    instance = EraseAndWriteAging(mock_shell)
    assert isinstance(instance, EraseAndWriteAging)


def test_erase_and_write_aging_succeeds(mocker):
    mock_shell = mocker.Mock()

    # LBA마다 읽은 값이 항상 쓰인 값과 같도록 설정
    fake_memory = {}

    def fake_write(cmd, isCommandFromScript):
        _, lba, data = cmd.split()
        fake_memory[lba] = data

    def fake_read(cmd, isCommandFromScript):
        _, lba = cmd.split()
        return fake_memory.get(lba, -1)

    def fake_erase(cmd, isCommandFromScript):
        _, start_lba, size = cmd.split()
        for lba in range(int(start_lba), int(start_lba) + int(size)):
            fake_memory[str(lba)] = '0x00000000'

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read
    mock_shell.erase.side_effect = fake_erase

    script = EraseAndWriteAging(mock_shell)
    result = script.run()

    assert result is True


def test_erase_and_write_aging_class_when_data_mismatch(mocker):
    mock_shell = mocker.Mock()

    def fake_write(cmd, isCommandFromScript):
        pass  # write 무시

    def fake_read(cmd, isCommandFromScript):
        return -1  # 항상 잘못된 값

    def fake_erase(cmd, isCommandFromScript):
        pass  # erase 무시

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read
    mock_shell.erase.side_effect = fake_erase

    script = EraseAndWriteAging(mock_shell)
    result = script.run()

    assert result is False

import pytest
from scripts.WriteReadAging import WriteReadAging

def test_partial_lba_write_class_can_be_instantiated():
    instance = WriteReadAging('test_interface')
    assert isinstance(instance, WriteReadAging)

def test_write_read_aging_succeeds(mocker):
    mock_shell = mocker.Mock()

    # LBA마다 읽은 값이 항상 쓰인 값과 같도록 설정
    lba_memory = {}

    def fake_write(addr, data):
        lba_memory[addr] = data

    def fake_read(addr):
        return lba_memory.get(addr, 0)

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read

    script = WriteReadAging(mock_shell)
    result = script.run()

    assert result is True

def test_write_read_aging_fails_when_data_mismatch(mocker):
    mock_shell = mocker.Mock()

    def fake_write(addr, data):
        pass  # write는 무시

    def fake_read(addr):
        return 0  # 항상 잘못된 값 반환

    mock_shell.write.side_effect = fake_write
    mock_shell.read.side_effect = fake_read

    script = WriteReadAging(mock_shell)
    result = script.run()

    assert result is False
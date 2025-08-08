import pytest
from scripts.WriteReadAging import WriteReadAging
from scripts.BaseScript import BaseScript

def test_partial_lba_write_class_can_be_instantiated(mocker):
    instance = WriteReadAging()
    assert isinstance(instance, WriteReadAging)


def test_write_read_aging_succeeds(mocker):

    # LBA마다 읽은 값이 항상 쓰인 값과 같도록 설정
    fake_memory = {}

    def fake_write(self, lba, data):
        fake_memory[lba] = data

    def fake_read(self, lba):
        return fake_memory.get(lba, 0x00000000)

    mocker.patch.object(BaseScript, 'read_lba', fake_read)
    mocker.patch.object(BaseScript, 'write_lba', fake_write)

    script = WriteReadAging()
    result = script.run()

    assert result is True


def test_write_read_aging_fails_when_data_mismatch(mocker):
    def fake_write(self, lba, data):
        pass  # write 무시

    def fake_read(self, lba):
        return -1  # 항상 잘못된 값

    mocker.patch.object(BaseScript, 'read_lba', fake_read)
    mocker.patch.object(BaseScript, 'write_lba', fake_write)

    script = WriteReadAging()
    result = script.run()

    assert result is False

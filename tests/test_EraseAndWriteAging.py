import pytest

from scripts.EraseAndWriteAging import EraseAndWriteAging
from scripts.BaseScript import BaseScript


def test_erase_and_write_aging_class_can_be_instantiated(mocker):
    instance = EraseAndWriteAging()
    assert isinstance(instance, EraseAndWriteAging)

def test_erase_and_write_aging_succeeds(mocker):
    fake_memory = {}

    def fake_write(self, lba, data):
        fake_memory[lba] = data

    def fake_read(self, lba):
        return fake_memory.get(lba, '0x00000000')

    def fake_erase(self, start_lba, size):
        for lba in range(start_lba, start_lba + size):
            fake_memory[lba] = '0x00000000'


    mocker.patch.object(BaseScript, 'read_lba', fake_read)
    mocker.patch.object(BaseScript, 'write_lba', fake_write)
    mocker.patch.object(BaseScript, 'erase_lba', fake_erase)

    script = EraseAndWriteAging()
    result = script.run()

    assert result is True

def test_erase_and_write_aging_class_when_data_mismatch(mocker):
    def fake_write(self, lba, data):
        pass  # write 무시

    def fake_read(self, lba):
        return -1  # 항상 잘못된 값

    def fake_erase(self,start_lba, size):
        pass  # erase 무시

    mocker.patch.object(BaseScript, 'read_lba', fake_read)
    mocker.patch.object(BaseScript, 'write_lba', fake_write)
    mocker.patch.object(BaseScript, 'erase_lba', fake_erase)


    script = EraseAndWriteAging()
    result = script.run()

    assert result is False
import pytest
from scripts.PartialLBAWrite import PartialLBAWrite
from scripts.BaseScript import BaseScript


def test_partial_lba_write_class_can_be_instantiated(mocker):
    instance = PartialLBAWrite()
    assert isinstance(instance, PartialLBAWrite)


def test_partial_lba_write_passes(mocker):
    fake_memory = {}

    def fake_write(self, lba, data):
        fake_memory[lba] = data

    def fake_read(self, lba):
        return fake_memory.get(lba, 0x00000000)

    mocker.patch.object(BaseScript, 'read_lba', fake_read)
    mocker.patch.object(BaseScript, 'write_lba', fake_write)

    script = PartialLBAWrite()
    result = script.run()

    assert result is True


def test_partial_lba_write_fails_on_mismatch(mocker):
    def fake_write(self, lba, data):
        pass  # write 무시

    def fake_read(self, lba):
        return -1  # 항상 잘못된 값

    mocker.patch.object(BaseScript, 'read_lba', fake_read)
    mocker.patch.object(BaseScript, 'write_lba', fake_write)

    script = PartialLBAWrite()
    result = script.run()

    assert result is False

import pytest
from scripts.WriteReadAging import WriteReadAging

def test_partial_lba_write_class_can_be_instantiated():
    instance = WriteReadAging('test_interface')
    assert isinstance(instance, WriteReadAging)

import pytest
from scripts.PartialLBAWrite import PartialLBAWrite

def test_partial_lba_write_class_can_be_instantiated():
    instance = PartialLBAWrite('test_interface')
    assert isinstance(instance, PartialLBAWrite)

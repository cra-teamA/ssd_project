import pytest
from unittest.mock import Mock
from scripts.FullWriteReadCompare import FullWriteReadCompare
from shell.shell import Shell

@pytest.fixture
def mock_shell_interface():
    mock= Mock(spec=Shell)
    return mock


def test_script_init(mock_shell_interface):
    script = FullWriteReadCompare(mock_shell_interface)
    assert script is not None
    assert script.shell is mock_shell_interface


def test_script_read_0(mock_shell_interface):
    script = FullWriteReadCompare(mock_shell_interface)
    script.run()

    mock_shell_interface.read.assert_called_once_with("R 0")

def test_script_write_0_0x00000000(mock_shell_interface):
    script = FullWriteReadCompare(mock_shell_interface)
    script.run()
    mock_shell_interface.write.assert_called_once_with("W 1 0x00000000")

def test_script_write_all(mock_shell_interface):
     script = FullWriteReadCompare(mock_shell_interface)
     script.run()
     mock_shell_interface.write.assert_any_call("W 1 0x00000000")
     mock_shell_interface.write.assert_any_call("W 11 0x00000000")
     mock_shell_interface.write.assert_any_call("W 31 0x00000000")
     mock_shell_interface.write.assert_any_call("W 55 0x00000000")
     mock_shell_interface.write.assert_any_call("W 99 0x00000000")

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

    mock_shell_interface.read.assert_called_once_with(0)

def test_script_write_0_0x00000000(mock_shell_interface):
    script = FullWriteReadCompare(mock_shell_interface)
    script.run()
    mock_shell_interface.write.assert_called_once_with(1,"0x00000000")

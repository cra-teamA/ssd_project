import pytest
from unittest.mock import Mock
from scripts.FullWriteReadCompare import Script1_FullWrite
from shell.shell import Shell

@pytest.fixture
def mock_shell_interface():
    mock= Mock(spec=Shell)
    return mock


def test_script1_init(mock_shell_interface):
    script = Script1_FullWrite(mock_shell_interface)
    assert script is not None
    assert script.shell is mock_shell_interface


def test_script1_read_0(mock_shell_interface):
    script = Script1_FullWrite(mock_shell_interface)
    script.run()

    mock_shell_interface.read.assert_called_once_with(0)


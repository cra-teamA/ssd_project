import pytest
from unittest.mock import Mock
from scripts.FullWriteReadCompare import Script1_FullWrite
from shell.shell import Shell

@pytest.fixture
def mock_shell_interface():
    mock= Mock(spec=Shell)
    return mock

def test_script1_full_write_init(mock_shell_interface):
    script = Script1_FullWrite(mock_shell_interface)
    assert script is not None
    assert script.shell is mock_shell_interface
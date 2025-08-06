import pytest
from unittest.mock import Mock
from scripts.FullWriteReadCompare import FullWriteReadCompare
from shell.shell import Shell

@pytest.fixture
def mock_shell_interface():
    mock= Mock(spec=Shell)
    return mock


@pytest.fixture
def mock_shell_interface_read_pass():
    mock = Mock()
    read_side_effect = []
    #read_side_effect = 0,0,0,0,0,1,1,1,1,1, ... ,19,19,19,19,19
    for group in range(20):
        value = f"0x{group:08x}"
        read_side_effect.extend([value] * 5)
    mock.read.side_effect = read_side_effect
    return mock

@pytest.fixture
def mock_shell_interface_read_fail():
    mock = Mock()
    read_side_effect = []
    #read_side_effect = 0,0,0,0,0,1,1,1,1,1, ... ,19,19,19,19,19
    for group in range(20):
        value = f"0x{group:08x}"
        read_side_effect.extend([value] * 5)
    read_side_effect[12]=f"0x{7:08x}"
    mock.read.side_effect = read_side_effect
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
    mock_shell_interface.write.assert_any_call("W 1 0x00000000")

def test_script_write_all_read_compare_pass(mock__read_shell_interface):
    script = FullWriteReadCompare(mock__read_shell_interface)
    script.run()
    assert mock__read_shell_interface.write.call_count == 100
    assert mock__read_shell_interface.read.call_count == 100

    for i, (w_call, r_call) in enumerate(zip(mock__read_shell_interface.write.call_args_list, mock__read_shell_interface.read.call_args_list)):
        group = i // 5
        expected_value = f"0x{group:08x}"
        expected_write = f"W {i} {expected_value}"
        expected_read = f"R {i}"
        assert w_call.args[0] == expected_write
        assert r_call.args[0] == expected_read

def test_script_write_all_read_compare_fail(mock_shell_interface_read_fail):
    script = FullWriteReadCompare(mock_shell_interface_read_fail)
    script.run()
    assert mock_shell_interface_read_fail.write.call_count == 15
    assert mock_shell_interface_read_fail.read.call_count == 13
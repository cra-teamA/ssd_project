import pytest
from unittest.mock import Mock
from scripts.FullWriteReadCompare import FullWriteReadCompare
from shell.shell import Shell

@pytest.fixture
def mock_dummy_shell_interface():
    mock = Mock(spec=Shell)
    return mock

@pytest.fixture
def mock_normal_shell_interface():
    mock = Mock(spec=Shell)
    def read_side_effect(cmd):
        lba = int(cmd.split()[1])
        group = lba // 5
        return f"0x{group:08x}"
    mock.read.side_effect = read_side_effect
    return mock

@pytest.fixture
def mock_compare_fail_shell_interface():
    mock = Mock(spec=Shell)
    def read_side_effect(cmd):
        lba = int(cmd.split()[1])
        if lba == 12:
            return "0x00000007"
        group = lba // 5
        return f"0x{group:08x}"
    mock.read.side_effect = read_side_effect
    return mock

def test_script_init(mock_dummy_shell_interface):
    script = FullWriteReadCompare(mock_dummy_shell_interface)
    assert script is not None
    assert script.shell is mock_dummy_shell_interface

def test_script_read_0(mock_dummy_shell_interface):
    script = FullWriteReadCompare(mock_dummy_shell_interface)
    script.run()
    mock_dummy_shell_interface.read.assert_any_call("read 0", True)

def test_script_write_0_0x00000000(mock_dummy_shell_interface):
    script = FullWriteReadCompare(mock_dummy_shell_interface)
    script.run()
    mock_dummy_shell_interface.write.assert_any_call("write 1 0x00000000")

def test_script_run_pass(mock_normal_shell_interface):
    script = FullWriteReadCompare(mock_normal_shell_interface)

    script.run()

    assert mock_normal_shell_interface.write.call_count == 100
    assert mock_normal_shell_interface.read.call_count == 100

    for i, (w_call, r_call) in enumerate(zip(mock_normal_shell_interface.write.call_args_list, mock_normal_shell_interface.read.call_args_list)):
        group = i // 5
        expected_value = f"0x{group:08x}"
        expected_write = f"write {i} {expected_value}"
        expected_read = f"read {i}"
        assert w_call.args[0] == expected_write
        assert r_call.args[0] == expected_read

def test_script_run_fail(mock_compare_fail_shell_interface):
    script = FullWriteReadCompare(mock_compare_fail_shell_interface)

    script.run()

    assert mock_compare_fail_shell_interface.write.call_count == 15
    assert mock_compare_fail_shell_interface.read.call_count == 13
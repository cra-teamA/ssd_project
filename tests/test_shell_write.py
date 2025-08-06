import pytest

from shell.shell import Shell
from unittest.mock import call

INVALID_MSG = "INVALID COMMAND\n"


@pytest.fixture
def shell_and_subprocess_mocker(mocker):
    shell = Shell()
    mock_run = mocker.patch("shell.shell.subprocess.run")
    return shell, mock_run


@pytest.mark.parametrize("value", ["0x0000BBBB", "0xBBBB"])
def test_shell_write(capsys, shell_and_subprocess_mocker, value):
    shell, mock_run = shell_and_subprocess_mocker
    shell.write(f"write 3 {value}")

    captured = capsys.readouterr()
    assert captured.out == "[Write] Done\n"
    mock_run.assert_called_once_with(["ssd", "W", "3", "0x0000BBBB"])


@pytest.mark.parametrize("lba", ["-1", "100"])
def test_shell_write_valid_check_lba(capsys, shell_and_subprocess_mocker, lba):
    shell, mock_run = shell_and_subprocess_mocker
    shell.write(f"write {lba} 0xAAAABBBB")

    captured = capsys.readouterr()
    assert captured.out == INVALID_MSG
    assert mock_run.call_count == 0

@pytest.mark.parametrize("value", ["0xAAAAABBBB", "0xAAAAFFFK", "AAAAFFF"])
def test_shell_write_valid_check_value(capsys, shell_and_subprocess_mocker, value):
    shell, mock_run = shell_and_subprocess_mocker

    
    shell.write(f"write 3 {value}")
    captured = capsys.readouterr()
    assert captured.out == INVALID_MSG
    assert mock_run.call_count == 0




@pytest.mark.parametrize("value", ["0x0000BBBB", "0xBBBB"])
def test_shell_fullwrite(capsys, shell_and_subprocess_mocker, value):
    shell, mock_run = shell_and_subprocess_mocker

    shell.fullwrite(f"write {value}")
    captured = capsys.readouterr()
    assert captured.out == "[FullWrite] Done\n"

    expected_calls = [
        call(["ssd", "W", str(i), "0x0000BBBB"]) for i in range(100)
    ]
    assert mock_run.call_args_list == expected_calls


@pytest.mark.parametrize("value", ["0xAAAAABBBB", "0xAAAAFFFK", "AAAAFFF"])
def test_shell_fullwrite_valid_check_value(capsys, shell_and_subprocess_mocker, value):
    shell, mock_run = shell_and_subprocess_mocker
   
    shell.fullwrite(f"write {value}")
    captured = capsys.readouterr()
    assert captured.out == INVALID_MSG
    assert mock_run.call_count == 0
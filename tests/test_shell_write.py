import pytest

from shell.shell import Shell
from unittest.mock import call

INVALID_MSG = "INVALID COMMAND\n"


@pytest.fixture
def shell_and_subprocess_mocker(mocker):
    shell = Shell()
    mock_run = mocker.patch("shell.shell.subprocess.run")
    return shell, mock_run


def test_shell_write(capsys, shell_and_subprocess_mocker):
    shell, mock_run = shell_and_subprocess_mocker
    shell.write("write 3 0xAAAABBBB")

    captured = capsys.readouterr()
    assert captured.out == "[Write] Done\n"
    mock_run.assert_called_once_with(["ssd", "W", "3", "0xAAAABBBB"])


def test_shell_write_valid_check_lba(capsys, shell_and_subprocess_mocker):
    shell, mock_run = shell_and_subprocess_mocker
    shell.write("write 1000 0xAAAABBBB")

    captured = capsys.readouterr()
    assert captured.out == INVALID_MSG
    assert mock_run.call_count == 0


def test_shell_write_valid_check_value(capsys, shell_and_subprocess_mocker):
    shell, mock_run = shell_and_subprocess_mocker

    shell.write("write 3 0xAAAAABBBB")
    captured = capsys.readouterr()
    assert captured.out == INVALID_MSG
    assert mock_run.call_count == 0

    shell.write("write 3 0xAAAAFFFK")
    captured = capsys.readouterr()
    assert captured.out == INVALID_MSG
    assert mock_run.call_count == 0

    shell.write("write 3 AAAAFFF")
    captured = capsys.readouterr()
    assert captured.out == INVALID_MSG
    assert mock_run.call_count == 0

    shell.write("write 3 0xBBBB")
    captured = capsys.readouterr()
    assert captured.out == "[Write] Done\n"
    mock_run.assert_called_once_with(["ssd", "W", "3", "0x0000BBBB"])


def test_shell_fullwrite(capsys, shell_and_subprocess_mocker):
    shell, mock_run = shell_and_subprocess_mocker

    shell.fullwrite("write 0xAAAABBBB")
    captured = capsys.readouterr()
    assert captured.out == "[FullWrite] Done\n"

    expected_calls = [
        call(["ssd", "W", str(i), "0xAAAABBBB"]) for i in range(100)
    ]
    assert mock_run.call_args_list == expected_calls

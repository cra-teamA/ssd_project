import pytest
from shell.shell import Shell


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


def test_shell_write_valid_check_address(capsys, shell_and_subprocess_mocker):
    shell, mock_run = shell_and_subprocess_mocker
    shell.write("write 1000 0xAAAABBBB")

    captured = capsys.readouterr()
    assert captured.out == "INVALID COMMAND\n"
    assert mock_run.call_count == 0

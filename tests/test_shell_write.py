import pytest
from shell.shell import Shell


def test_shell_write(capsys, mocker):
    shell = Shell()
    mock_run = mocker.patch("shell.shell.subprocess.run")
    shell.write("write 3 0xAAAABBBB")

    captured = capsys.readouterr()
    assert captured.out == "[Write] Done\n"
    mock_run.assert_called_once_with(["ssd", "W", "3", "0xAAAABBBB"])
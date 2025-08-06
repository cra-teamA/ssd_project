import pytest
from pytest_mock import mocker
from shell.shell import Shell


def test_shell_exit(mocker, capsys):
    shell = Shell()
    mocker.patch("builtins.input", return_value="exit")
    mocker_exit = mocker.patch("sys.exit")
    shell.exit()
    output = capsys.readouterr()
    mocker_exit.assert_called_once_with(0)
    assert output.out == "Exiting shell...\n"

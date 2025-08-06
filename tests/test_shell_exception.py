from unittest.mock import mock_open
import pytest
from pytest_mock import mocker, MockerFixture
from shell.shell import Shell, is_valid_command


def test_shell_command_valid(mocker):
    mocker.patch("builtins.input", return_value="write")
    ret = is_valid_command()
    assert ret is True


def test_shell_command_invalid_foramt(mocker, capsys):
    mocker.patch("builtins.input", return_value="hello")
    is_valid_command()
    output = capsys.readouterr()
    assert output.out == 'INVALID COMMAND\n'

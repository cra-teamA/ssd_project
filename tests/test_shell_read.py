from unittest.mock import mock_open
from pytest_mock import mocker, MockerFixture
from shell.shell import Shell
import pytest


def test_shell_read_valid_format(mocker: MockerFixture, capsys):
    mock_subprocess = mocker.patch("shell.shell.subprocess.run")
    fake_output_content = "0xAAAABBBC\n"
    mocker.patch(
        "builtins.open",
        mock_open(read_data=fake_output_content)
    )
    shell = Shell()
    shell.read("read 3")
    captured = capsys.readouterr()

    mock_subprocess.assert_called_once_with(
        ["ssd", "R", "3"],
        capture_output=True,
        text=True
    )
    assert captured.out == "[Read] LBA 3 : 0xAAAABBBC\n"


def test_shell_read_invalid_format(mocker):
    mocker.patch("builtins.input", return_value="read 3")
    fake_output_content = "0xAAAABBBC\n"
    mocker.patch(
        "builtins.open",
        mock_open(read_data=fake_output_content)
    )
    shell = Shell()
    with pytest.raises(ValueError):
        shell.read("read a 150")
    with pytest.raises(ValueError):
        shell.read("read")


def test_shell_valid_lba(mocker):
    mocker.patch("builtins.input", return_value="read 3")
    mock_subprocess = mocker.patch("shell.shell.subprocess.run")
    fake_output_content = "0xAAAABBBC\n"
    mocker.patch(
        "builtins.open",
        mock_open(read_data=fake_output_content)
    )
    shell = Shell()
    result = shell.read("read 3")
    assert result == "0xAAAABBBC"


def test_shell_invalid_lba(mocker):
    shell = Shell()
    with pytest.raises(ValueError):
        shell.read("read 150")  # 150은 범위 벗어남
    with pytest.raises(ValueError):
        shell.read("read abc")  # 숫자 아님

def test_shell_is_script(mocker, capsys):
    shell = Shell()
    mock_subprocess = mocker.patch("shell.shell.subprocess.run")
    fake_output_content = "0xAAAABBBC\n"
    mocker.patch(
        "builtins.open",
        mock_open(read_data=fake_output_content)
    )
    line = shell.read("read 3", True)
    output = capsys.readouterr()

    assert output.out == ""
    assert line == "0xAAAABBBC"

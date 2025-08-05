from unittest.mock import mock_open
from pytest_mock import mocker
from shell.shell import Shell


def test_shell_read(mocker, capsys):
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
        ["python", "ssd.py", "R", "3"],
        capture_output=True,
        text=True
    )
    assert captured.out == "[Read] LBA 3 : 0xAAAABBBC\n"

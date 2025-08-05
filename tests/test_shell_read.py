from unittest.mock import mock_open
from shell.shell import Shell


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
        capture_output=True,
        text=True
    )
    assert captured.out == "[Read] LBA 3 : 0xAAAABBBC\n"

from unittest.mock import mock_open
import pytest
from pytest_mock import mocker, MockerFixture
from shell.shell import Shell, is_valid_command, SSD_OUTPUT_PATH, SSD_COMMAND
from unittest.mock import call


@pytest.fixture
def shell_and_subprocess_mocker(mocker: MockerFixture):
    shell = Shell()
    mock_run = mocker.patch("shell.shell.subprocess.run")
    return shell, mock_run


def test_shell_command_valid(mocker: MockerFixture):
    mocker.patch("builtins.input", return_value="write")
    ret = is_valid_command()
    assert ret is True


def test_shell_command_invalid_foramt(mocker: MockerFixture, capsys):
    mocker.patch("builtins.input", return_value="hello")
    ret = is_valid_command()
    output = capsys.readouterr()
    assert output.out == 'INVALID COMMAND\n'
    assert ret is False


def test_shell_exit(mocker: MockerFixture, capsys):
    shell = Shell()
    mocker_exit = mocker.patch("sys.exit")
    shell.exit()
    output = capsys.readouterr()
    mocker_exit.assert_called_once_with(0)
    assert output.out == "Exiting shell...\n"


def test_shell_full_read_valid(mocker: MockerFixture, capsys):
    mk_full_read = mocker.patch('shell.shell.Shell._read')
    mk_full_read.return_value = '0x00000000'
    shell = Shell()
    shell.full_read()
    captured = capsys.readouterr()
    assert mk_full_read.call_count == 100
    mk_full_read.assert_has_calls([call(x) for x in range(100)])
    assert captured.out.strip() == '[Full Read]\n' + '\n'.join([f"LBA {i:02d} : 0x00000000" for i in range(100)])


def test_shell_help(capsys):
    shell = Shell()
    shell.help()
    captured = capsys.readouterr()
    assert captured.out == ('\n'
                            '        제작자: [Team All Clear] 장진섭 팀장, 박성일, 이규홍, 최준식, 임소현, 이휘은\n'
                            '        명령어 사용 법 :\n'
                            '         1. read: read [LBA]\n'
                            '         2. write: write [LBA] [VALUE]\n'
                            '         3. fullwrite: fullwrite [VALUE]\n'
                            '         4. fullread: fullread\n'
                            '         5. 1_FullWriteAndReadCompare: 1_ 혹은 1_FullWriteAndReadCompare 입력\n'
                            '         6. 2_PartialLBAWrite: 2_ 혹은 2_PartialLBAWrite 입력\n'
                            '         7. 3_WriteReadAging: 3_ 혹은 3_WriteReadAging 입력\n'
                            '         8. exit: exit\n'
                            '        그 외 명령어 입력 시, INVALID COMMAND 가 출력 됩니다.\n')


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
        [SSD_COMMAND, "R", "3"],
        capture_output=True,
        text=True
    )
    assert captured.out == "[Read] LBA 3 : 0xAAAABBBC\n"


def test_shell_read_invalid_format(mocker: MockerFixture):
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


def test_shell_valid_lba(mocker: MockerFixture):
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


def test_shell_invalid_lba(mocker: MockerFixture):
    shell = Shell()
    with pytest.raises(ValueError):
        shell.read("read 150")  # 150은 범위 벗어남
    with pytest.raises(ValueError):
        shell.read("read abc")  # 숫자 아님


def test_shell_is_script(mocker: MockerFixture, capsys):
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


@pytest.mark.parametrize("value", ["0x0000BBBB", "0xBBBB"])
def test_shell_write_cmd_success(capsys, shell_and_subprocess_mocker, value):
    shell, mock_run = shell_and_subprocess_mocker
    shell.write(f"write 3 {value}")

    captured = capsys.readouterr()
    assert captured.out == "[Write] Done\n"
    mock_run.assert_called_once_with([SSD_COMMAND, "W", "3", "0x0000BBBB"])


@pytest.mark.parametrize("value", ["0x0000BBBB", "0xBBBB"])
def test_shell_write_script_success(capsys, shell_and_subprocess_mocker, value):
    shell, mock_run = shell_and_subprocess_mocker
    shell.write(f"write 3 {value}", True)

    captured = capsys.readouterr()
    assert captured.out == ""
    mock_run.assert_called_once_with([SSD_COMMAND, "W", "3", "0x0000BBBB"])


@pytest.mark.parametrize("lba", ["-1", "100"])
def test_shell_write_valid_check_lba_fail(shell_and_subprocess_mocker, lba):
    shell, mock_run = shell_and_subprocess_mocker

    with pytest.raises(ValueError):
        shell.write(f"write {lba} 0xAAAABBBB")
    assert mock_run.call_count == 0


@pytest.mark.parametrize("value", ["0xAAAAABBBB", "0xAAAAFFFK", "AAAAFFF"])
def test_shell_write_valid_check_value_fail(shell_and_subprocess_mocker, value):
    shell, mock_run = shell_and_subprocess_mocker

    with pytest.raises(ValueError):
        shell.write(f"write 3 {value}")
    assert mock_run.call_count == 0


@pytest.mark.parametrize("value", ["0x0000BBBB", "0xBBBB"])
def test_shell_fullwrite_success(capsys, shell_and_subprocess_mocker, value):
    shell, mock_run = shell_and_subprocess_mocker

    shell.fullwrite(f"write {value}")
    captured = capsys.readouterr()
    assert captured.out == "[FullWrite] Done\n"

    expected_calls = [
        call([SSD_COMMAND, "W", str(i), "0x0000BBBB"]) for i in range(100)
    ]
    assert mock_run.call_args_list == expected_calls


@pytest.mark.parametrize("value", ["0xAAAAABBBB", "0xAAAAFFFK", "AAAAFFF"])
def test_shell_fullwrite_valid_check_value_fail(shell_and_subprocess_mocker, value):
    shell, mock_run = shell_and_subprocess_mocker

    with pytest.raises(ValueError):
        shell.fullwrite(f"write {value}")
    assert mock_run.call_count == 0

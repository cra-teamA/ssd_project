from unittest.mock import mock_open, patch, call
from pytest_mock import MockerFixture
from shell.shell import Shell

def test_shell_full_read_valid(mocker: MockerFixture, capsys):
    mk_full_read = mocker.patch('shell.shell.Shell._read')
    mk_full_read.return_value = '0x00000000'
    shell = Shell()
    shell.full_read()
    captured = capsys.readouterr()
    assert mk_full_read.call_count == 100
    mk_full_read.assert_has_calls([call(x) for x in range(100)])
    assert captured.out.strip() == '[Full Read]\n' + '\n'.join([f"LBA {i:02d} : 0x00000000" for i in range(100)])


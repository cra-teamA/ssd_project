import pytest
from unittest.mock import MagicMock, patch

from shell.shell import Shell


@pytest.fixture
def shell():
    return Shell()


@patch("scripts.FullWriteReadCompare.FullWriteReadCompare")
def test_run_script_full_write_read_compare(mock_script, shell, capsys):
    instance = MagicMock()
    instance.run.return_value = True
    mock_script.return_value = instance

    shell.run_script("1_FullWriteReadCompare")

    captured = capsys.readouterr()
    assert "PASS" in captured.out
    instance.run.assert_called_once()


@patch("scripts.PartialLBAWrite.PartialLBAWrite")
def test_run_script_partial_lba_write(mock_script, shell, capsys):
    instance = MagicMock()
    instance.run.return_value = False
    mock_script.return_value = instance

    shell.run_script("2_PartialLBAWrite")

    captured = capsys.readouterr()
    assert "FAIL" in captured.out
    instance.run.assert_called_once()


@patch("scripts.WriteReadAging.WriteReadAging")
def test_run_script_write_read_aging(mock_script, shell, capsys):
    instance = MagicMock()
    instance.run.return_value = False
    mock_script.return_value = instance

    shell.run_script("3_WriteReadAging")

    captured = capsys.readouterr()
    assert "FAIL" in captured.out
    instance.run.assert_called_once()
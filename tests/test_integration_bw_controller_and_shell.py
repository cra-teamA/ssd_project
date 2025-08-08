from shell.shell import Shell
import pytest
import json
import os

# 현재 테스트 파일 위치 기준으로 루트 디렉토리 계산
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SSD_NAND_PATH = os.path.join(PROJECT_ROOT, 'ssd_nand.txt')
SSD_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'ssd_output.txt')
SINGLE_TEST_DATA = {1:"0xaaaaaaa1"}
ERROR = 'ERROR'

@pytest.fixture
def shell_with_single_data():
    shell = Shell()
    shell.flush("flush")
    with open(SSD_NAND_PATH, "w", encoding="utf-8") as f:
        json.dump(SINGLE_TEST_DATA, f, ensure_ascii=False)
    return shell

def get_ssd_output():
    with open(SSD_OUTPUT_PATH, "r", encoding="utf-8") as f:
        actual = f.read()
    return actual

def test_shell_read_cmd_success(capsys, shell_with_single_data):
    shell = shell_with_single_data
    shell.read(f"read 1")

    captured = capsys.readouterr()
    assert captured.out == "[Read] LBA 1 : 0xaaaaaaa1\n"

def test_shell_read_cmd_new_address(capsys, shell_with_single_data):
    shell = shell_with_single_data
    shell.read(f"read 2")

    captured = capsys.readouterr()
    assert captured.out == "[Read] LBA 2 : 0x00000000\n"

@pytest.mark.parametrize('value', ['-1', 'a', None])
def test_shell_read_cmd_invalid_address(shell_with_single_data, value):
    shell = shell_with_single_data
    with pytest.raises(ValueError):
        shell.read(f"read {value}")

@pytest.mark.parametrize("addr, value", [(0,"0x0000BBBB"), (1,"0xBBBB")])
def test_shell_write_script_success(capsys, shell_with_single_data, addr, value):
    shell = shell_with_single_data
    shell.write(f"write {addr} {value}", True)

    captured = capsys.readouterr()
    assert captured.out == ""

    shell.read(f"read {addr}")
    captured = capsys.readouterr()
    value = f"0x{int(value, 16) :08X}".lower()
    assert captured.out == f"[Read] LBA {addr} : {value}\n"

@pytest.mark.parametrize("value", ["0x0000BBBB", "0xBBBB"])
def test_shell_write_cmd_success(capsys, shell_with_single_data, value):
    shell = shell_with_single_data
    shell.write(f"write 3 {value}")
    captured = capsys.readouterr()
    assert captured.out == "[Write] Done\n"

@pytest.mark.parametrize("addr, value", [(-1,"0x0000BBBB"), (100,"0xBBBB")])
def test_shell_write_cmd_invalid_address(shell_with_single_data, addr, value):
    shell = shell_with_single_data
    with pytest.raises(ValueError):
        shell.write(f"write {addr} {value}", True)
    # assert get_ssd_output() == ERROR

@pytest.mark.parametrize("addr, value", [(0,"0xZ"), (1,"0x000000000")])
def test_shell_write_cmd_invalid_value(shell_with_single_data, addr, value):
    shell = shell_with_single_data
    with pytest.raises(ValueError):
        shell.write(f"write {addr} {value}", True)
    # assert get_ssd_output() == ERROR

@pytest.mark.parametrize("addr, value", [(0,"0xZ"), (1,"0x000000000")])
def test_shell_write_cmd_invalid_value(shell_with_single_data, addr, value):
    shell = shell_with_single_data
    with pytest.raises(ValueError):
        shell.write(f"write {addr} {value}", True)
    # assert get_ssd_output() == ERROR

def test_shell_full_write_and_full_read(capsys, shell_with_single_data):
    shell = Shell()
    value = '0x0000BBBB'.lower()
    shell.fullwrite(f"fullwrite {value}")
    captured = capsys.readouterr()
    assert captured.out == "[FullWrite] Done\n"

    shell.fullread(f"fullread")
    captured = capsys.readouterr()
    assert captured.out.strip() == '[Full Read]\n' + '\n'.join([f"LBA {i:02d} : {value}" for i in range(100)])

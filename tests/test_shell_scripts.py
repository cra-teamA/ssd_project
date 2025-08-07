import pytest

from shell.shell import Shell
from scripts.FullWriteReadCompare import FullWriteReadCompare
from scripts.PartialLBAWrite import PartialLBAWrite
from scripts.WriteReadAging import WriteReadAging


@pytest.fixture
def shell():
    return Shell()


def test_run_script_pass(mocker, shell):
    # 각 스크립트 run()이 True 리턴하도록 패치
    for command, cls in [
        ("1_FullWriteReadCompare", FullWriteReadCompare),
        ("2_PartialLBAWrite", PartialLBAWrite),
        ("3_WriteReadAging", WriteReadAging),
    ]:
        run_mock = mocker.patch.object(cls, "run", return_value=True)
        print_mock = mocker.patch("builtins.print")

        shell.run_script(command)

        run_mock.assert_called_once()
        print_mock.assert_called_with("PASS")

def test_run_script_fail(mocker, shell):
    # run()이 False 반환하는 경우 테스트
    run_mock = mocker.patch.object(FullWriteReadCompare, "run", return_value=False)
    print_mock = mocker.patch("builtins.print")

    shell.run_script("1_FullWriteReadCompare")

    run_mock.assert_called_once()
    print_mock.assert_called_with("FAIL")

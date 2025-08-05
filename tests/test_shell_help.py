from unittest.mock import mock_open
from shell.shell import Shell

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

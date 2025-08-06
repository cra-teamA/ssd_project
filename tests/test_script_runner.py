import pytest
from unittest.mock import Mock
from scripts.ScriptRunner import ScriptRunner

@pytest.mark.parametrize(
    "command, idx, expected_called",
    [
        ("1_FullWriteReadCompare", "1", True),
        ("2_PartialLBAWrite", "2", True),
        ("3_WriteReadAging", "3", True),
        ("4_WriteReadAging", "4", False),
        ("3_", "2", False),
        ("3_", "2", False),
        ("3_", "3", True),
        ("2_", "2", True),
        ("1_", "1", True),
        ("_", "1", False),
        ("avads_aa", "1", False),
    ]
)
def test_script_run_called(command, idx, expected_called):
    mock_instance = Mock()

    # 원래 클래스 백업
    original_class = ScriptRunner.script_mapping.get(idx)

    if expected_called:
        # mocking only if the script should be called
        ScriptRunner.script_mapping[idx] = lambda shell: mock_instance

    mock_shell = Mock()
    runner = ScriptRunner(mock_shell)
    runner.run(command)

    if expected_called:
        mock_instance.run.assert_called_once()
    else:
        mock_instance.run.assert_not_called()

    # 원래 클래스 복구
    if expected_called:
        ScriptRunner.script_mapping[idx] = original_class
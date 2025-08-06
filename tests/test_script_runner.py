import pytest
from unittest.mock import Mock
from scripts.ScriptRunner import ScriptRunner

@pytest.mark.parametrize(
    "command, idx",
    [
        ("1_FullWriteReadCompare", "1"),
        ("2_PartialLBAWrite", "2"),
        ("3_WriteReadAging", "3"),
    ]
)
def test_script_run_called(command, idx):
    mock_instance = Mock()

    original_class = ScriptRunner.script_mapping[idx]
    ScriptRunner.script_mapping[idx] = lambda shell: mock_instance

    mock_shell = Mock()
    runner = ScriptRunner(mock_shell)

    runner.run(command)

    mock_instance.run.assert_called_once()

    # 원래 클래스 복구
    ScriptRunner.script_mapping[idx] = original_class
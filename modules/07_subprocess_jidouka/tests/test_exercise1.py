"""演習1のテスト: run_command"""
import sys

from exercises.exercise1 import run_command


def test_echo_returncode_is_zero():
    returncode, _stdout = run_command(["echo", "hello"])
    assert returncode == 0


def test_echo_stdout_contains_expected_text():
    _returncode, stdout = run_command(["echo", "hello"])
    assert stdout.strip() == "hello"


def test_returns_tuple_of_int_and_str():
    result = run_command(["echo", "type-check"])
    assert isinstance(result, tuple)
    assert len(result) == 2
    returncode, stdout = result
    assert isinstance(returncode, int)
    assert isinstance(stdout, str)


def test_python_print_stdout():
    # sys.executable を使うことで、どの環境でも確実に存在するpython3を
    # 呼び出せる(外部コマンドへの依存を避ける)。
    _returncode, stdout = run_command(
        [sys.executable, "-c", "print('subprocess-test-123')"]
    )
    assert "subprocess-test-123" in stdout


def test_nonzero_exit_code_is_captured():
    returncode, _stdout = run_command(
        [sys.executable, "-c", "import sys; sys.exit(3)"]
    )
    assert returncode == 3

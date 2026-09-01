"""演習2のテスト: is_command_successful"""
import sys

from exercises.exercise2 import is_command_successful


def test_echo_is_successful():
    assert is_command_successful(["echo", "ok"]) is True


def test_python_exit_zero_is_successful():
    assert is_command_successful([sys.executable, "-c", "exit(0)"]) is True


def test_python_exit_nonzero_is_not_successful():
    assert is_command_successful([sys.executable, "-c", "exit(1)"]) is False


def test_python_raises_exception_is_not_successful():
    # 例外が発生して終了した場合もreturncodeは0以外になる
    assert (
        is_command_successful([sys.executable, "-c", "raise ValueError('boom')"])
        is False
    )

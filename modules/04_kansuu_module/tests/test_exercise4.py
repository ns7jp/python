"""演習4のテスト: measure_time デコレーター"""
from exercises.exercise4 import measure_time


def test_return_value_is_preserved():
    @measure_time
    def add(a, b):
        return a + b

    assert add(2, 3) == 5


def test_wrapped_function_name_is_preserved():
    @measure_time
    def sample_function():
        return "ok"

    # functools.wraps を使っていれば __name__ が元の関数名のまま保たれる
    assert sample_function.__name__ == "sample_function"


def test_prints_execution_time(capsys):
    @measure_time
    def noop():
        return None

    noop()
    captured = capsys.readouterr()
    assert "実行時間" in captured.out

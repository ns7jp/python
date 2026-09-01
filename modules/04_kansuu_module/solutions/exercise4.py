"""演習4の模範解答: 関数の実行時間を計測するデコレーター

仕様の詳細はexercises/exercise4.pyのdocstringを参照してください。
"""
import functools
import time


def measure_time(func):
    """関数の実行時間を計測し、標準出力に表示するデコレーター。

    仕様はexercises/exercise4.pyのdocstringを参照。
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[実行時間] {func.__name__}: {elapsed:.3f}秒")
        return result

    return wrapper

"""演習4(応用): 関数の実行時間を計測するデコレーターを作る

デコレーターは、既存の関数の前後に処理を追加できる仕組みです。
サーバー運用の現場でも、「処理にかかった時間を計測してログに残す」
といった目的でよく使われます。functools.wraps を使い、元の関数の
情報(__name__ など)を保ったままラップする方法を学びます。
"""
import functools
import time


def measure_time(func):
    """関数の実行時間を計測し、標準出力に表示するデコレーター。

    ラップされた関数(func)を呼び出す際、実行前後の時刻を計測し、
        "[実行時間] 関数名: X.XXX秒"
    という形式でprint()を使って表示する。その上で、元の関数の戻り値を
    そのまま呼び出し元に返す(戻り値を変えてはいけない)。

    functools.wraps(func) を使って、ラップ後の関数(wrapper)が元の関数の
    __name__ などの情報を保つようにすること。

    引数:
        func (callable): 実行時間を計測したい対象の関数。

    戻り値:
        callable: 実行時間の計測とprint出力を行うラップ後の関数(wrapper)。
            wrapper を呼び出すと、func(*args, **kwargs) の戻り値が
            そのまま返る。

    入出力例:
        >>> @measure_time
        ... def add(a, b):
        ...     return a + b
        >>> add(1, 2)  # 標準出力に "[実行時間] add: 0.000秒" のように表示される
        3
    """
    # TODO: functools.wraps(func) を使ったラッパー関数 wrapper(*args, **kwargs)
    #       を定義してください。wrapper の中では、
    #         1. time.perf_counter() などで実行前の時刻を記録する
    #         2. func(*args, **kwargs) を呼び出して結果を受け取る
    #         3. 実行後の時刻との差から経過時間を計算する
    #         4. 「[実行時間] 関数名: X.XXX秒」の形式でprintする
    #            (関数名は func.__name__ で取得できます)
    #         5. 2.で受け取った結果をそのまま返す
    #       という処理を行い、最後に wrapper を返してください。
    raise NotImplementedError("measure_time を実装してください")

"""演習2の模範解答: 複数のレスポンスタイムから平均値を求める

仕様の詳細はexercises/exercise2.pyのdocstringを参照してください。
"""


def average_response_time(*response_times_ms):
    """複数のレスポンスタイム(ミリ秒)の平均値を計算する。

    仕様はexercises/exercise2.pyのdocstringを参照。
    """
    if not response_times_ms:
        return 0.0
    return round(sum(response_times_ms) / len(response_times_ms), 2)

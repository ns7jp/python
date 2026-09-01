"""演習4の模範解答: 稼働率(アップタイム率)の計算"""


def calculate_uptime_rate(check_results):
    """定期ヘルスチェックの結果リストから稼働率(%)を計算する。

    詳しい仕様は exercises/exercise4.py の docstring を参照してください。
    """
    if len(check_results) == 0:
        return 0.0

    success_count = 0
    for result in check_results:
        if result:
            success_count += 1

    rate = success_count / len(check_results) * 100
    return round(rate, 2)

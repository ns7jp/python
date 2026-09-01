"""演習4(応用): 稼働率(アップタイム率)の計算

定期的なヘルスチェック(死活監視)の結果は、成功(True)・失敗(False)の
リストとして記録されることがよくあります。この演習では for 文を使って
リストを集計し、稼働率(%)を計算する関数を実装します。
"""


def calculate_uptime_rate(check_results):
    """定期ヘルスチェックの結果リストから稼働率(%)を計算する。

    for文でリストを1つずつ確認し、成功(True)の数を数えて
    「成功数 ÷ 全体数 × 100」で稼働率を計算する。

    引数:
        check_results (list[bool]): 各回のヘルスチェック結果のリスト。
            True が成功、False が失敗を表す。

    戻り値:
        float: 稼働率(%)。小数点第2位までで四捨五入(round)する。
            リストが空の場合は 0.0 を返す。

    入出力例:
        >>> calculate_uptime_rate([True, True, True, False])
        75.0
        >>> calculate_uptime_rate([True, True, True])
        100.0
        >>> calculate_uptime_rate([False, False])
        0.0
        >>> calculate_uptime_rate([])
        0.0
        >>> calculate_uptime_rate([True, True, False])
        66.67
    """
    # TODO: for文で check_results を1つずつ確認し、成功数をカウントしてください。
    #       リストが空の場合は 0.0 を返すことを忘れずに。
    #       稼働率 = 成功数 / 全体数 * 100 を round(値, 2) で丸めてください。
    raise NotImplementedError("calculate_uptime_rate を実装してください")

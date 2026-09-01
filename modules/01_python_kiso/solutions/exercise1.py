"""
演習1 模範解答: ディスク使用率の計算とパーセント表示
"""


def calc_disk_usage_percent(used_gb, total_gb):
    """ディスクの使用容量と総容量から、使用率(%)を計算する。

    使用率は「使用量 ÷ 総量 × 100」で計算し、round()を使って
    小数点第2位までに丸めたfloat値を返すこと。

    total_gb が 0 の場合は、0での割り算(ゼロ除算)を避けるため、
    計算をせずに 0.0 を返すこと。

    引数:
        used_gb (float or int): 使用中のディスク容量(GB単位)
        total_gb (float or int): ディスクの総容量(GB単位)

    戻り値:
        float: 小数点第2位までround()した使用率(%)。
               total_gbが0のときは0.0。

    入出力例:
        >>> calc_disk_usage_percent(50, 100)
        50.0
        >>> calc_disk_usage_percent(1, 3)
        33.33
        >>> calc_disk_usage_percent(0, 0)
        0.0
    """
    # total_gb が 0 の場合はゼロ除算を避けて 0.0 を返す
    if total_gb == 0:
        return 0.0

    percent = used_gb / total_gb * 100
    return round(percent, 2)


def format_percent(percent):
    """数値を受け取り、「12.34%」のような文字列に整形して返す。

    f-stringの書式指定 `:.2f` を使って、小数点第2位まで表示する
    パーセント文字列を作ること。

    引数:
        percent (float or int): パーセントを表す数値

    戻り値:
        str: 「12.34%」のような、小数点第2位までのパーセント文字列

    入出力例:
        >>> format_percent(12.3)
        '12.30%'
        >>> format_percent(5)
        '5.00%'
        >>> format_percent(100)
        '100.00%'
    """
    return f"{percent:.2f}%"

"""
演習4(応用): メモリ使用率のアラートメッセージ生成 (難易度: ★★★)

算術演算子・比較演算子・f-stringを組み合わせて、実務に近い
「監視メッセージ生成」処理を練習します。
"""


def memory_alert_message(used_mb, total_mb, threshold_percent=80.0):
    """メモリ使用率を計算し、閾値を超えていれば警告文、超えていなければ正常文を返す。

    使用率(%)は「used_mb ÷ total_mb × 100」で計算する
    (total_mb が 0 以下の場合はゼロ除算を避けるため使用率を 0.0 として扱うこと)。

    使用率が threshold_percent より大きい(超えている)場合は、
        "警告: メモリ使用率が{使用率:.2f}%です"
    という形式の文字列を返すこと。

    使用率が threshold_percent 以下(閾値と同じ場合を含む)の場合は、
        "正常: メモリ使用率は{使用率:.2f}%です"
    という形式の文字列を返すこと。

    (上の{使用率:.2f}の部分は、f-stringの :.2f 書式で
    小数点第2位まで表示した数値に置き換えること)

    引数:
        used_mb (float or int): 使用中のメモリ容量(MB単位)
        total_mb (float or int): メモリの総容量(MB単位)
        threshold_percent (float): 警告を出す閾値(%)。デフォルトは80.0

    戻り値:
        str: 「警告: メモリ使用率が90.00%です」または
             「正常: メモリ使用率は50.00%です」のようなメッセージ文字列

    入出力例:
        >>> memory_alert_message(7200, 8000)
        '警告: メモリ使用率が90.00%です'
        >>> memory_alert_message(4000, 8000)
        '正常: メモリ使用率は50.00%です'
        >>> memory_alert_message(4800, 8000, threshold_percent=60.0)
        '正常: メモリ使用率は60.00%です'
        >>> memory_alert_message(100, 0)
        '正常: メモリ使用率は0.00%です'
    """
    # TODO: total_mb が 0 以下の場合は使用率を 0.0 として扱う
    # TODO: 使用率(%)を計算する(used_mb / total_mb * 100)
    # TODO: 使用率が threshold_percent より大きいかどうかで、
    #       返すメッセージ(f-string)を分岐させる
    raise NotImplementedError("memory_alert_message を実装してください")

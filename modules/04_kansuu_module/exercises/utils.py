"""演習3で使う補助モジュール。

celsius_to_status はこのモジュールにすでに実装されています。
(この関数自体は「モジュール分割」の演習の主眼ではないため、
完成した状態で用意しています。exercise3.py からこの関数をimportして
使ってください。)
"""


def celsius_to_status(temp):
    """気温(セ氏温度)を受け取り、データセンターの状態を表す文字列を返す。

    判定基準:
        temp が 20 未満           -> "低温注意"
        20 <= temp <= 28          -> "正常"
        temp が 28 を超える        -> "高温注意"

    引数:
        temp (int | float): 気温(℃)。

    戻り値:
        str: "低温注意" / "正常" / "高温注意" のいずれか。

    入出力例:
        >>> celsius_to_status(15)
        '低温注意'
        >>> celsius_to_status(24)
        '正常'
        >>> celsius_to_status(30)
        '高温注意'
    """
    if temp < 20:
        return "低温注意"
    elif temp <= 28:
        return "正常"
    else:
        return "高温注意"

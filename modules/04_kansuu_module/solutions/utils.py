"""演習3で使う補助モジュールの模範解答。

仕様の詳細は exercises/utils.py のdocstringを参照してください。
"""


def celsius_to_status(temp):
    """気温(セ氏温度)を受け取り、データセンターの状態を表す文字列を返す。

    仕様はexercises/utils.pyのdocstringを参照。
    """
    if temp < 20:
        return "低温注意"
    elif temp <= 28:
        return "正常"
    else:
        return "高温注意"

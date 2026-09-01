"""
演習2 模範解答: 稼働時間(uptime)を日本語表記に変換する
"""


def seconds_to_hms(total_seconds):
    """経過秒数(サーバーのuptimeを想定)を、日本語の時間表記に変換する。

    1日 = 86400秒、1時間 = 3600秒、1分 = 60秒として、
    // (整数除算) と % (剰余) を使って日・時間・分・秒に分解し、
    「1日2時間3分4秒」のような文字列を組み立てて返すこと。

    ただし、日数が0の場合は「日」の部分を省略し、
    「2時間3分4秒」のように表示すること(時間・分・秒は
    0であっても省略せず表示する)。

    引数:
        total_seconds (int): 経過秒数(0以上の整数を想定)

    戻り値:
        str: 「1日2時間3分4秒」または(0日のときは)「2時間3分4秒」の形式の文字列

    入出力例:
        >>> seconds_to_hms(93784)
        '1日2時間3分4秒'
        >>> seconds_to_hms(7384)
        '2時間3分4秒'
        >>> seconds_to_hms(0)
        '0時間0分0秒'
    """
    # 念のため整数に変換しておく(float が渡された場合は切り捨てる)
    total_seconds = int(total_seconds)

    days = total_seconds // 86400
    remainder = total_seconds % 86400

    hours = remainder // 3600
    remainder = remainder % 3600

    minutes = remainder // 60
    seconds = remainder % 60

    if days > 0:
        return f"{days}日{hours}時間{minutes}分{seconds}秒"
    else:
        return f"{hours}時間{minutes}分{seconds}秒"

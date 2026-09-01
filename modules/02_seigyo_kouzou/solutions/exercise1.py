"""演習1の模範解答: ポート番号を分類する"""


def check_port_status(port):
    """ポート番号を受け取り、その種類を表す文字列を返す。

    詳しい仕様は exercises/exercise1.py の docstring を参照してください。
    """
    if port < 0 or port > 65535:
        return "無効なポート"
    elif port <= 1023:
        return "システムポート"
    elif port <= 49151:
        return "登録済みポート"
    else:
        return "動的ポート"

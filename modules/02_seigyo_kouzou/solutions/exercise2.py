"""演習2の模範解答: サーバーステータスの集計"""


def summarize_server_statuses(statuses):
    """ステータス文字列のリストから、各ステータスの出現回数を集計する。

    詳しい仕様は exercises/exercise2.py の docstring を参照してください。
    """
    result = {}
    for status in statuses:
        if status in result:
            result[status] = result[status] + 1
        else:
            result[status] = 1
    return result

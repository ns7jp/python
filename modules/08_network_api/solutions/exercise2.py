"""演習2の模範解答: requestsライブラリで外部APIやWebサーバーの状態を確認する

仕様の詳細はexercises/exercise2.pyのdocstringを参照してください。
"""
import requests


def check_http_status(url, http_get=None):
    """指定したURLにGETリクエストを送り、HTTPステータスコードを返す。

    仕様はexercises/exercise2.pyのdocstringを参照。
    """
    getter = http_get if http_get is not None else requests.get
    try:
        response = getter(url)
        return response.status_code
    except Exception:
        # タイムアウト・接続エラーなど、通信中に起こりうる様々な例外を
        # まとめて捕まえ、呼び出し元にはNoneとして伝える
        return None

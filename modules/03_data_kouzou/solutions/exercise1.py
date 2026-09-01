"""演習1の模範解答: 稼働中のサーバーだけを取り出す"""


def filter_active_servers(servers):
    """サーバー情報のリストから、稼働中(status == "active")のサーバー名だけを抜き出す。

    詳しい仕様は exercises/exercise1.py の docstring を参照してください。
    """
    return [server["name"] for server in servers if server["status"] == "active"]

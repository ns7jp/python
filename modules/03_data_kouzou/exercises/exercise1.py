"""演習1: 稼働中のサーバーだけを取り出す

サーバー監視の現場では、複数台のサーバー情報をまとめて管理し、その中から
「稼働中(active)のサーバーだけ」を抜き出したい場面がよくあります。
この演習では、リスト内包表記(list comprehension)を使ってその処理を実装します。
"""


def filter_active_servers(servers):
    """サーバー情報のリストから、稼働中(status == "active")のサーバー名だけを抜き出す。

    servers は辞書のリストで、各要素は次の形をしている。
        {"name": "サーバー名(str)", "status": "状態を表す文字列(str)"}

    status が "active" である要素だけを対象に、その "name" の値を
    元のリストの並び順のまま新しいリストとして返す。

    リスト内包表記( [式 for 要素 in リスト if 条件] という書き方)を
    使って実装すること。

    引数:
        servers (list[dict]): サーバー情報の辞書のリスト。
            各辞書は {"name": str, "status": str} の形。

    戻り値:
        list[str]: status が "active" であるサーバーの name だけを集めたリスト。

    入出力例:
        >>> filter_active_servers([
        ...     {"name": "web01", "status": "active"},
        ...     {"name": "web02", "status": "stopped"},
        ...     {"name": "db01", "status": "active"},
        ... ])
        ['web01', 'db01']

        >>> filter_active_servers([])
        []
    """
    # TODO: リスト内包表記を使って、status が "active" のサーバーの name だけを
    #       集めたリストを返してください。
    raise NotImplementedError("filter_active_servers を実装してください")

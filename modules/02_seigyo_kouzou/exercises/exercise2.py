"""演習2: サーバーステータスの集計

複数台のサーバーを監視していると、"ok"（正常）、"error"（異常）、
"warning"（警告）といったステータス文字列のリストが得られることがよく
あります。この演習では for 文と if 文だけを使って、それぞれのステータスが
何回出現したかを数える関数を実装します。
"""


def summarize_server_statuses(statuses):
    """ステータス文字列のリストから、各ステータスの出現回数を集計する。

    for文とif文だけを使って実装すること
    (collections.Counter や辞書内包表記は、まだ習っていない前提なので使わない)。

    引数:
        statuses (list[str]): サーバーのステータスを表す文字列のリスト。
            例: ["ok", "ok", "error", "warning"]

    戻り値:
        dict: キーがステータス文字列、値がその出現回数(int)の辞書。
            出現したステータスだけをキーとして含めればよい。

    入出力例:
        >>> summarize_server_statuses(["ok", "ok", "error", "warning"])
        {'ok': 2, 'error': 1, 'warning': 1}
        >>> summarize_server_statuses([])
        {}
        >>> summarize_server_statuses(["ok", "ok", "ok"])
        {'ok': 3}
    """
    # TODO: for文で statuses を1つずつ見て、辞書に集計してください。
    #       すでに辞書にキーがあるかどうかを if 文で判定しましょう。
    raise NotImplementedError("summarize_server_statuses を実装してください")

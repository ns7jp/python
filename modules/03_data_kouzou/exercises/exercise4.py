"""演習4(応用): 負荷が高いサーバーを上位N件だけ取り出す

負荷分散(ロードバランシング)や障害対応の現場では、「CPU負荷が高い順に
サーバーを並べて、対応が必要な上位のサーバーだけを確認したい」という
場面がよくあります。この演習では sorted() の key引数とスライスを使って、
その処理を実装します。
"""


def top_n_servers_by_load(servers, n):
    """CPU負荷が高い順にサーバーを並べ替え、上位n件を返す。

    servers は辞書のリストで、各要素は次の形をしている。
        {"name": "サーバー名(str)", "cpu_load": CPU負荷を表す数値(int または float)}

    cpu_load の値が大きい順(降順)にサーバーを並べ替え、
    先頭からn件(辞書のリスト)を返す。

    sorted() の key引数(並べ替えの基準を指定する引数)と、
    スライス([:n] のような書き方で一部分だけ取り出す方法)を使って
    実装すること。

    n が servers の件数より大きい場合は、servers 全体を並べ替えた
    結果をそのまま返す(エラーにはしない)。

    引数:
        servers (list[dict]): サーバー情報の辞書のリスト。
            各辞書は {"name": str, "cpu_load": int または float} の形。
        n (int): 取り出す件数。

    戻り値:
        list[dict]: cpu_loadの降順に並べ替えた、上位n件のサーバー情報のリスト。
            元の辞書と同じ形({"name": ..., "cpu_load": ...})の要素からなる。

    入出力例:
        >>> servers = [
        ...     {"name": "web01", "cpu_load": 45.0},
        ...     {"name": "web02", "cpu_load": 92.5},
        ...     {"name": "db01", "cpu_load": 60.0},
        ... ]
        >>> top_n_servers_by_load(servers, 2)
        [{'name': 'web02', 'cpu_load': 92.5}, {'name': 'db01', 'cpu_load': 60.0}]
    """
    # TODO: sorted()のkey引数を使ってcpu_loadの降順に並べ替え、
    #       スライスを使って上位n件を返してください。
    raise NotImplementedError("top_n_servers_by_load を実装してください")

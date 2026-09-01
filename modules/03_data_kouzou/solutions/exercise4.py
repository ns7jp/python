"""演習4の模範解答: 負荷が高いサーバーを上位N件だけ取り出す"""


def top_n_servers_by_load(servers, n):
    """CPU負荷が高い順にサーバーを並べ替え、上位n件を返す。

    詳しい仕様は exercises/exercise4.py の docstring を参照してください。
    """
    sorted_servers = sorted(servers, key=lambda server: server["cpu_load"], reverse=True)
    return sorted_servers[:n]

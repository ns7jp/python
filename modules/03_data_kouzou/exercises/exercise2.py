"""演習2: サービス名とポート番号の対応表(辞書)を扱う

サーバー運用では「このサービスは何番ポートを使っているか」「このポート番号は
どのサービスのものか」を素早く調べたい場面がよくあります。この演習では、
タプルのリストから辞書を作る処理と、辞書を逆引きする処理を実装します。
"""


def build_service_port_map(pairs):
    """(サービス名, ポート番号) のタプルのリストから、辞書を作って返す。

    pairs は (サービス名, ポート番号) というタプルのリスト。
    これを {サービス名: ポート番号} という形の辞書に変換して返す。

    同じサービス名が複数回登場した場合は、後に出てきた方の値で
    上書きされる(通常の辞書の代入と同じ挙動でよい)。

    引数:
        pairs (list[tuple[str, int]]): (サービス名, ポート番号) のタプルのリスト。

    戻り値:
        dict[str, int]: {サービス名: ポート番号} の辞書。

    入出力例:
        >>> build_service_port_map([("ssh", 22), ("http", 80), ("https", 443)])
        {'ssh': 22, 'http': 80, 'https': 443}

        >>> build_service_port_map([])
        {}
    """
    # TODO: pairs を1つずつ処理し、{サービス名: ポート番号} の辞書を作って返してください。
    raise NotImplementedError("build_service_port_map を実装してください")


def find_service_by_port(port_map, port):
    """ポート番号から、対応するサービス名を逆引きして返す。

    port_map は build_service_port_map() が返すような
    {サービス名: ポート番号} の辞書。この中から、値(ポート番号)が
    引数 port と一致するキー(サービス名)を探して返す。

    一致するサービスが見つからない場合は None を返す。
    複数のサービスが同じポート番号を持つことは通常ないため、
    最初に見つかったサービス名を返せばよい。

    引数:
        port_map (dict[str, int]): {サービス名: ポート番号} の辞書。
        port (int): 調べたいポート番号。

    戻り値:
        str または None: portに対応するサービス名。見つからない場合は None。

    入出力例:
        >>> port_map = {"ssh": 22, "http": 80, "https": 443}
        >>> find_service_by_port(port_map, 80)
        'http'
        >>> find_service_by_port(port_map, 9999) is None
        True
    """
    # TODO: port_map の中から、値が port と一致するキーを探して返してください。
    #       見つからない場合は None を返してください。
    raise NotImplementedError("find_service_by_port を実装してください")

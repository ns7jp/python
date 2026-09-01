"""演習2の模範解答: サービス名とポート番号の対応表(辞書)を扱う"""


def build_service_port_map(pairs):
    """(サービス名, ポート番号) のタプルのリストから、辞書を作って返す。

    詳しい仕様は exercises/exercise2.py の docstring を参照してください。
    """
    port_map = {}
    for name, port in pairs:
        port_map[name] = port
    return port_map


def find_service_by_port(port_map, port):
    """ポート番号から、対応するサービス名を逆引きして返す。

    詳しい仕様は exercises/exercise2.py の docstring を参照してください。
    """
    for name, mapped_port in port_map.items():
        if mapped_port == port:
            return name
    return None

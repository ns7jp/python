"""
演習4: サーバー情報を管理するクラス(fixtureで使うテスト対象)

この章の exercises/ には、すでに完成した「テスト対象のコード」が
入っています。学習者が編集するのは tests/ 側です。
"""


class ServerRegistry:
    """
    サーバー名とサーバー情報を対応付けて管理するレジストリ(登録簿)。

    実際のインフラ運用では、管理対象のサーバー一覧(ホスト名、IPアドレス、
    役割など)を何らかの形で一元管理する必要があります。このクラスは
    その最小限の仕組みを、Pythonの辞書(dict)を使って表現したものです。

    属性:
        _servers (dict): サーバー名(str)をキー、サーバー情報(任意の値。
            通常はdict)を値とする辞書。
    """

    def __init__(self):
        """レジストリを空の状態で初期化する。"""
        self._servers = {}

    def add_server(self, name, info):
        """
        サーバーを登録する。

        すでに同じ名前のサーバーが登録されている場合は、情報を上書きする。

        引数:
            name (str): サーバー名(例: "web01")。
            info: サーバーに関する情報(通常はdict)。

        戻り値:
            None

        入出力例:
            >>> reg = ServerRegistry()
            >>> reg.add_server("web01", {"ip": "192.168.0.1"})
        """
        self._servers[name] = info

    def get_server(self, name):
        """
        登録済みのサーバー情報を取得する。

        引数:
            name (str): サーバー名。

        戻り値:
            登録されていればその情報を返す。登録されていなければNoneを返す。

        入出力例:
            >>> reg = ServerRegistry()
            >>> reg.add_server("web01", {"ip": "192.168.0.1"})
            >>> reg.get_server("web01")
            {'ip': '192.168.0.1'}
            >>> reg.get_server("unknown") is None
            True
        """
        return self._servers.get(name)

    def list_names(self):
        """
        登録済みの全サーバー名をリストで返す。

        戻り値:
            list[str]: 登録済みサーバー名のリスト(登録した順序)。

        入出力例:
            >>> reg = ServerRegistry()
            >>> reg.add_server("web01", {})
            >>> reg.add_server("db01", {})
            >>> reg.list_names()
            ['web01', 'db01']
        """
        return list(self._servers.keys())

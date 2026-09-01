"""
演習4のテスト雛形: ServerRegistryクラスをテストしよう(fixtureの練習) 📝

pytestのfixture(フィクスチャ)を使うと、複数のテスト関数で共通して
使いたい「準備済みのデータ」を1か所にまとめて、使い回すことができます。
ここでは、あらかじめ2〜3件のサーバーが登録された ServerRegistry
インスタンスをfixtureとして用意し、それを使って get_server /
list_names をテストします。

fixtureの書き方の例:

    @pytest.fixture
    def registry():
        reg = ServerRegistry()
        reg.add_server("web01", {"ip": "192.168.0.1"})
        reg.add_server("db01", {"ip": "192.168.0.2"})
        return reg

このように @pytest.fixture デコレーターを付けた関数を定義しておくと、
テスト関数の引数に同じ名前(ここでは registry)を書くだけで、
pytestが自動的にこの関数を呼び出し、その戻り値を渡してくれます。

    def test_something(registry):
        ...  # ここで registry (準備済みのServerRegistry) を使える
"""

import pytest

from exercises.exercise4 import ServerRegistry


# TODO: 上のコメントを参考にして、@pytest.fixture デコレーターを使った
#       registry という名前のfixture関数を実装しよう。
#       ServerRegistryのインスタンスを作り、add_serverで2〜3件の
#       サーバーを登録してから、そのインスタンスをreturnすること。
#
# @pytest.fixture
# def registry():
#     reg = ServerRegistry()
#     reg.add_server("web01", {"ip": "192.168.0.1"})
#     reg.add_server("db01", {"ip": "192.168.0.2"})
#     return reg


def test_get_server_returns_registered_info(registry):
    """
    登録済みのサーバー名を渡すと、get_serverが正しい情報を返すことを
    確認する。
    """
    # TODO: registryフィクスチャを使って、get_server("web01") などが
    #       登録時に渡した情報(dict)と一致することをassert文で確認しよう
    pass


def test_get_server_returns_none_for_unknown_name(registry):
    """
    未登録のサーバー名を渡すと、get_serverがNoneを返すことを確認する。
    """
    # TODO: get_server("unknown-server") の戻り値が None になることを
    #       assert文で確認しよう
    pass


def test_list_names_returns_all_registered_names(registry):
    """
    list_namesが、登録済みの全サーバー名を返すことを確認する。
    """
    # TODO: list_names() の戻り値に、fixtureで登録した全てのサーバー名
    #       (例: "web01", "db01")が含まれていることをassert文で確認しよう
    pass

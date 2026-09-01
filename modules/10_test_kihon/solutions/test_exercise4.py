"""
演習4 模範解答: ServerRegistryクラスのテスト(fixtureの利用)
"""

import pytest

from exercises.exercise4 import ServerRegistry


@pytest.fixture
def registry():
    """2件のサーバーがあらかじめ登録されたServerRegistryを返すfixture。"""
    reg = ServerRegistry()
    reg.add_server("web01", {"ip": "192.168.0.1", "role": "web"})
    reg.add_server("db01", {"ip": "192.168.0.2", "role": "db"})
    return reg


def test_get_server_returns_registered_info(registry):
    """登録済みのサーバー名を渡すと、get_serverが正しい情報を返す。"""
    assert registry.get_server("web01") == {"ip": "192.168.0.1", "role": "web"}
    assert registry.get_server("db01") == {"ip": "192.168.0.2", "role": "db"}


def test_get_server_returns_none_for_unknown_name(registry):
    """未登録のサーバー名を渡すと、get_serverはNoneを返す。"""
    assert registry.get_server("unknown-server") is None


def test_list_names_returns_all_registered_names(registry):
    """list_namesが登録済みの全サーバー名を返す。"""
    names = registry.list_names()
    assert "web01" in names
    assert "db01" in names
    assert len(names) == 2

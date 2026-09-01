"""演習1(filter_active_servers)のテスト。"""
from exercises.exercise1 import filter_active_servers


def test_filter_basic():
    servers = [
        {"name": "web01", "status": "active"},
        {"name": "web02", "status": "stopped"},
        {"name": "db01", "status": "active"},
    ]
    assert filter_active_servers(servers) == ["web01", "db01"]


def test_filter_all_active():
    servers = [
        {"name": "a", "status": "active"},
        {"name": "b", "status": "active"},
    ]
    assert filter_active_servers(servers) == ["a", "b"]


def test_filter_no_active():
    servers = [
        {"name": "a", "status": "stopped"},
        {"name": "b", "status": "maintenance"},
    ]
    assert filter_active_servers(servers) == []


def test_filter_empty_list():
    assert filter_active_servers([]) == []


def test_filter_preserves_order():
    servers = [
        {"name": "z", "status": "active"},
        {"name": "y", "status": "active"},
        {"name": "x", "status": "stopped"},
        {"name": "w", "status": "active"},
    ]
    assert filter_active_servers(servers) == ["z", "y", "w"]


def test_filter_returns_list_type():
    result = filter_active_servers([{"name": "a", "status": "active"}])
    assert isinstance(result, list)

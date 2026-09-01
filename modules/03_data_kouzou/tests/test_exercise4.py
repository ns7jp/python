"""演習4(top_n_servers_by_load)のテスト。"""
from exercises.exercise4 import top_n_servers_by_load


def test_top_n_basic():
    servers = [
        {"name": "web01", "cpu_load": 45.0},
        {"name": "web02", "cpu_load": 92.5},
        {"name": "db01", "cpu_load": 60.0},
    ]
    result = top_n_servers_by_load(servers, 2)
    assert result == [
        {"name": "web02", "cpu_load": 92.5},
        {"name": "db01", "cpu_load": 60.0},
    ]


def test_top_n_all_servers():
    servers = [
        {"name": "a", "cpu_load": 10},
        {"name": "b", "cpu_load": 30},
        {"name": "c", "cpu_load": 20},
    ]
    result = top_n_servers_by_load(servers, 3)
    assert result == [
        {"name": "b", "cpu_load": 30},
        {"name": "c", "cpu_load": 20},
        {"name": "a", "cpu_load": 10},
    ]


def test_top_n_larger_than_list():
    servers = [
        {"name": "a", "cpu_load": 10},
        {"name": "b", "cpu_load": 30},
    ]
    result = top_n_servers_by_load(servers, 10)
    assert result == [
        {"name": "b", "cpu_load": 30},
        {"name": "a", "cpu_load": 10},
    ]


def test_top_n_zero():
    servers = [{"name": "a", "cpu_load": 10}]
    assert top_n_servers_by_load(servers, 0) == []


def test_top_n_empty_list():
    assert top_n_servers_by_load([], 3) == []


def test_top_n_does_not_mutate_input():
    servers = [
        {"name": "a", "cpu_load": 10},
        {"name": "b", "cpu_load": 30},
    ]
    original_order = list(servers)
    top_n_servers_by_load(servers, 1)
    assert servers == original_order


def test_top_n_returns_list_type():
    servers = [{"name": "a", "cpu_load": 10}]
    result = top_n_servers_by_load(servers, 1)
    assert isinstance(result, list)

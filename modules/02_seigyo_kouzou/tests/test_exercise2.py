"""演習2(summarize_server_statuses)のテスト。"""
from exercises.exercise2 import summarize_server_statuses


def test_basic_summary():
    statuses = ["ok", "ok", "error", "warning"]
    assert summarize_server_statuses(statuses) == {"ok": 2, "error": 1, "warning": 1}


def test_empty_list():
    assert summarize_server_statuses([]) == {}


def test_all_same_status():
    assert summarize_server_statuses(["ok", "ok", "ok"]) == {"ok": 3}


def test_single_element():
    assert summarize_server_statuses(["error"]) == {"error": 1}


def test_does_not_mutate_input():
    statuses = ["ok", "error"]
    original = list(statuses)
    summarize_server_statuses(statuses)
    assert statuses == original

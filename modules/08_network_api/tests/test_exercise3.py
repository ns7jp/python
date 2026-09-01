"""演習3のテスト: parse_server_status_json"""
from exercises.exercise3 import parse_server_status_json


def test_parse_server_status_json_all_keys_present():
    text = '{"status": "ok", "cpu": 42, "memory": 70}'
    assert parse_server_status_json(text) == {"status": "ok", "cpu": 42, "memory": 70}


def test_parse_server_status_json_extra_key_is_ignored():
    text = '{"status": "ok", "disk": 90}'
    assert parse_server_status_json(text) == {"status": "ok"}


def test_parse_server_status_json_only_some_keys_present():
    text = '{"cpu": 55}'
    assert parse_server_status_json(text) == {"cpu": 55}


def test_parse_server_status_json_invalid_json_returns_empty_dict():
    assert parse_server_status_json("これはJSONではありません") == {}


def test_parse_server_status_json_empty_string_returns_empty_dict():
    assert parse_server_status_json("") == {}


def test_parse_server_status_json_non_object_json_returns_empty_dict():
    # トップレベルが配列(list)のJSONは辞書ではないので空の辞書を返す
    assert parse_server_status_json("[1, 2, 3]") == {}


def test_parse_server_status_json_no_relevant_keys():
    text = '{"foo": "bar"}'
    assert parse_server_status_json(text) == {}

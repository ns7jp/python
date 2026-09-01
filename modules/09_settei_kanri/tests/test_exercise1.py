"""演習1 load_json_config のテスト"""

import json
import os

from exercises.exercise1 import load_json_config


def test_load_json_config_existing_file(tmp_path):
    """存在するJSONファイルを正しく読み込めること"""
    data = {"host": "localhost", "port": 8080, "debug": True}
    file_path = tmp_path / "config.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load_json_config(str(file_path))

    assert result == data


def test_load_json_config_missing_file(tmp_path):
    """存在しないファイルを指定した場合は空の辞書を返すこと"""
    file_path = tmp_path / "not_exist.json"

    result = load_json_config(str(file_path))

    assert result == {}


def test_load_json_config_nested_structure(tmp_path):
    """入れ子構造を持つJSONも正しく読み込めること"""
    data = {
        "database": {"host": "db.example.com", "port": 5432},
        "features": ["a", "b", "c"],
    }
    file_path = tmp_path / "nested.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load_json_config(str(file_path))

    assert result == data
    assert isinstance(result["database"], dict)


def test_load_json_config_empty_object(tmp_path):
    """中身が空のJSONオブジェクトの場合は空の辞書を返すこと"""
    file_path = tmp_path / "empty.json"
    file_path.write_text("{}", encoding="utf-8")

    result = load_json_config(str(file_path))

    assert result == {}

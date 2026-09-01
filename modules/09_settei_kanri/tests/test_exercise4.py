"""演習4 build_environment_config のテスト"""

from exercises.exercise4 import build_environment_config


def test_build_environment_config_with_override():
    """overridesに対応する環境があれば、その差分で上書きされること"""
    base = {"debug": True, "log_level": "INFO", "port": 8000}
    overrides = {
        "prod": {"debug": False, "log_level": "WARNING"},
    }

    result = build_environment_config("prod", base, overrides)

    assert result == {"debug": False, "log_level": "WARNING", "port": 8000}


def test_build_environment_config_without_matching_override():
    """overridesにその環境名が無ければbase_configのコピーがそのまま返ること"""
    base = {"debug": True, "log_level": "INFO", "port": 8000}
    overrides = {
        "prod": {"debug": False, "log_level": "WARNING"},
    }

    result = build_environment_config("dev", base, overrides)

    assert result == base


def test_build_environment_config_does_not_mutate_base_config():
    """base_config自体が書き換えられないこと"""
    base = {"debug": True, "log_level": "INFO", "port": 8000}
    base_snapshot = dict(base)
    overrides = {
        "prod": {"debug": False, "log_level": "WARNING"},
    }

    build_environment_config("prod", base, overrides)

    assert base == base_snapshot


def test_build_environment_config_returns_new_object():
    """戻り値がbase_configとは別のオブジェクトであること"""
    base = {"debug": True}
    overrides = {}

    result = build_environment_config("dev", base, overrides)

    assert result == base
    assert result is not base


def test_build_environment_config_can_add_new_key():
    """overridesに新しいキーがあれば、base_configに無くても追加されること"""
    base = {"debug": True}
    overrides = {
        "staging": {"feature_flag_x": True},
    }

    result = build_environment_config("staging", base, overrides)

    assert result == {"debug": True, "feature_flag_x": True}


def test_build_environment_config_empty_overrides():
    """overridesが空の辞書の場合はbase_configのコピーが返ること"""
    base = {"debug": True, "port": 8000}

    result = build_environment_config("prod", base, {})

    assert result == base
    assert result is not base

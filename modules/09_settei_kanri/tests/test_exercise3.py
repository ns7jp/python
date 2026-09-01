"""演習3 resolve_setting のテスト"""

from exercises.exercise3 import resolve_setting


def test_resolve_setting_env_has_priority():
    """envにキーがある場合は、envの値が最優先になること"""
    env = {"PORT": "9000"}
    config = {"PORT": "8080"}

    result = resolve_setting("PORT", env, config, 80)

    assert result == "9000"


def test_resolve_setting_falls_back_to_config():
    """envにキーが無く、configにある場合はconfigの値が使われること"""
    env = {}
    config = {"PORT": "8080"}

    result = resolve_setting("PORT", env, config, 80)

    assert result == "8080"


def test_resolve_setting_falls_back_to_default():
    """envにもconfigにも無い場合はdefaultが使われること"""
    env = {}
    config = {}

    result = resolve_setting("PORT", env, config, 80)

    assert result == 80


def test_resolve_setting_env_and_config_have_different_keys():
    """他のキーの存在に影響されず、指定したkeyだけで判定すること"""
    env = {"HOST": "example.com"}
    config = {"PORT": "8080"}

    # PORTはenvに無いのでconfigの値、HOSTはenvにあるのでenvの値になる
    assert resolve_setting("PORT", env, config, 80) == "8080"
    assert resolve_setting("HOST", env, config, "localhost") == "example.com"


def test_resolve_setting_does_not_mutate_inputs():
    """env や config の中身が関数呼び出しによって変更されないこと"""
    env = {"PORT": "9000"}
    config = {"PORT": "8080"}
    env_copy = dict(env)
    config_copy = dict(config)

    resolve_setting("PORT", env, config, 80)

    assert env == env_copy
    assert config == config_copy

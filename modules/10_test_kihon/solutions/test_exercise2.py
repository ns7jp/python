"""
演習2 模範解答: is_valid_hostname関数のテスト
"""

from exercises.exercise2 import is_valid_hostname


def test_is_valid_hostname_valid_cases():
    """有効なホスト名の例をテストする。"""
    assert is_valid_hostname("web01.example.com") is True
    assert is_valid_hostname("db-01") is True
    assert is_valid_hostname("192.168.0.1") is True
    assert is_valid_hostname("a") is True


def test_is_valid_hostname_invalid_cases():
    """無効なホスト名の例をテストする。"""
    assert is_valid_hostname("") is False
    assert is_valid_hostname("web_01") is False
    assert is_valid_hostname("-web01") is False
    assert is_valid_hostname("web01-") is False
    assert is_valid_hostname("a" * 254) is False

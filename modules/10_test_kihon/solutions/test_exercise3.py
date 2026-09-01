"""
演習3 模範解答: parse_port関数のテスト(例外のテスト)
"""

import pytest

from exercises.exercise3 import parse_port


def test_parse_port_valid_value():
    """正常系: 有効な文字列を渡すと正しいintのポート番号が返る。"""
    assert parse_port("8080") == 8080
    assert isinstance(parse_port("8080"), int)
    assert parse_port("0") == 0
    assert parse_port("65535") == 65535


def test_parse_port_invalid_string_raises_value_error():
    """異常系: 数字でない文字列を渡すとValueErrorが発生する。"""
    with pytest.raises(ValueError):
        parse_port("abc")


def test_parse_port_out_of_range_raises_value_error():
    """異常系: 範囲外の値を渡すとValueErrorが発生する。"""
    with pytest.raises(ValueError):
        parse_port("70000")
    with pytest.raises(ValueError):
        parse_port("-1")

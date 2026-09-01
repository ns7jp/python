"""演習1のテスト: safe_divide, parse_int_safe"""
from exercises.exercise1 import parse_int_safe, safe_divide


def test_safe_divide_normal_case():
    assert safe_divide(10, 2) == 5.0


def test_safe_divide_by_zero_returns_none():
    assert safe_divide(10, 0) is None


def test_safe_divide_negative_numbers():
    assert safe_divide(-9, 3) == -3.0


def test_parse_int_safe_valid_string():
    assert parse_int_safe("42") == 42


def test_parse_int_safe_negative_string():
    assert parse_int_safe("-7") == -7


def test_parse_int_safe_invalid_string_returns_none():
    assert parse_int_safe("abc") is None


def test_parse_int_safe_empty_string_returns_none():
    assert parse_int_safe("") is None


def test_parse_int_safe_float_like_string_returns_none():
    # "12.5" は int() にそのまま渡すとValueErrorになる文字列
    assert parse_int_safe("12.5") is None

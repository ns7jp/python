"""
演習3のテスト雛形: parse_port関数をテストしよう(例外のテスト) 📝

正常系(正しいポート番号文字列を渡すと正しいintが返る)と、
異常系(不正な文字列や範囲外の値を渡すとValueErrorが発生する)の
両方をテストします。

異常系(例外が発生することを確認したいテスト)には、
pytest.raises を使います。書き方の例:

    with pytest.raises(ValueError):
        何か例外が起きるはずの処理()

この with ブロックの中で指定した例外(ここではValueError)が
実際に発生すればテストは成功し、発生しなければテストは失敗します。
"""

import pytest

from exercises.exercise3 import parse_port


def test_parse_port_valid_value():
    """
    正常系: 有効な文字列を渡すと、正しいintのポート番号が返ることを確認する。

    例: "8080" -> 8080 (int型)
    """
    # TODO: parse_port("8080") の戻り値が 8080 になることを
    #       assert文で確認しよう。int型であることも確認できるとなお良い
    # ヒント: assert parse_port("8080") == 8080
    pass


def test_parse_port_invalid_string_raises_value_error():
    """
    異常系: 数字でない文字列を渡すと ValueError が発生することを確認する。

    例: "abc" のような文字列。
    """
    # TODO: with pytest.raises(ValueError): のブロックの中で
    #       parse_port("abc") を呼び出し、ValueErrorが発生することを
    #       確認しよう
    pass


def test_parse_port_out_of_range_raises_value_error():
    """
    異常系: 範囲外(0〜65535の外)の値を渡すと ValueError が発生することを
    確認する。

    例: "70000" や "-1" など。
    """
    # TODO: pytest.raises(ValueError) を使って、parse_port("70000") や
    #       parse_port("-1") がValueErrorになることを確認しよう
    pass

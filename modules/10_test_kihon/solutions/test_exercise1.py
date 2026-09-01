"""
演習1 模範解答: bytes_to_gb関数のテスト
"""

from exercises.exercise1 import bytes_to_gb


def test_bytes_to_gb_normal_case():
    """通常のケース: 1073741824バイトは1.0GBになる。"""
    assert bytes_to_gb(1073741824) == 1.0


def test_bytes_to_gb_zero_bytes():
    """0バイトは0.0GBになる。"""
    assert bytes_to_gb(0) == 0.0

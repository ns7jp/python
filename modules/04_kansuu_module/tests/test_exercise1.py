"""演習1のテスト: human_readable_bytes"""
from exercises.exercise1 import human_readable_bytes


def test_bytes_under_1024():
    assert human_readable_bytes(512) == "512B"


def test_zero_bytes():
    assert human_readable_bytes(0) == "0B"


def test_boundary_1024_is_kilobytes():
    assert human_readable_bytes(1024) == "1.00KB"


def test_kilobytes():
    assert human_readable_bytes(1536) == "1.50KB"


def test_megabytes():
    assert human_readable_bytes(2 * 1024 * 1024) == "2.00MB"


def test_gigabytes():
    assert human_readable_bytes(3 * 1024 ** 3) == "3.00GB"

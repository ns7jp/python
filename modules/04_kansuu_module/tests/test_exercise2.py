"""演習2のテスト: average_response_time"""
from exercises.exercise2 import average_response_time


def test_multiple_values():
    assert average_response_time(100, 200, 300) == 200.0


def test_rounding_to_two_decimal_places():
    assert average_response_time(120.5, 130.25) == 125.38


def test_no_arguments_returns_zero():
    assert average_response_time() == 0.0


def test_single_value():
    assert average_response_time(50) == 50.0

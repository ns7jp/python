"""演習4(calculate_uptime_rate)のテスト。"""
from exercises.exercise4 import calculate_uptime_rate


def test_all_success():
    assert calculate_uptime_rate([True, True, True]) == 100.0


def test_all_failure():
    assert calculate_uptime_rate([False, False]) == 0.0


def test_empty_list():
    assert calculate_uptime_rate([]) == 0.0


def test_partial_success_75_percent():
    assert calculate_uptime_rate([True, True, True, False]) == 75.0


def test_rounding_to_two_decimal_places():
    # 2/3 = 66.666...% -> 小数点第2位までで四捨五入して 66.67
    assert calculate_uptime_rate([True, True, False]) == 66.67


def test_single_success():
    assert calculate_uptime_rate([True]) == 100.0

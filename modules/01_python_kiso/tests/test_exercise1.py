"""演習1のテスト: ディスク使用率の計算とパーセント表示"""

from exercises.exercise1 import calc_disk_usage_percent, format_percent


def test_calc_disk_usage_percent_basic():
    assert calc_disk_usage_percent(50, 100) == 50.0


def test_calc_disk_usage_percent_rounding():
    # 1 / 3 * 100 = 33.333... -> 小数点第2位までround()すると33.33
    assert calc_disk_usage_percent(1, 3) == 33.33


def test_calc_disk_usage_percent_full():
    assert calc_disk_usage_percent(100, 100) == 100.0


def test_calc_disk_usage_percent_zero_total():
    # total_gb が 0 のときは 0.0 を返す(ゼロ除算を避ける)
    assert calc_disk_usage_percent(0, 0) == 0.0
    assert calc_disk_usage_percent(50, 0) == 0.0


def test_calc_disk_usage_percent_returns_float():
    result = calc_disk_usage_percent(50, 100)
    assert isinstance(result, float)


def test_format_percent_basic():
    assert format_percent(12.3) == "12.30%"


def test_format_percent_integer_input():
    assert format_percent(5) == "5.00%"


def test_format_percent_hundred():
    assert format_percent(100) == "100.00%"


def test_format_percent_zero():
    assert format_percent(0) == "0.00%"

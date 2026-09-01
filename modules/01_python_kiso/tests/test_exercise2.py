"""演習2のテスト: 稼働時間(uptime)を日本語表記に変換する"""

from exercises.exercise2 import seconds_to_hms


def test_seconds_to_hms_with_days():
    # 93784秒 = 1日2時間3分4秒 (86400 + 7200 + 180 + 4)
    assert seconds_to_hms(93784) == "1日2時間3分4秒"


def test_seconds_to_hms_without_days():
    # 7384秒 = 2時間3分4秒 (7200 + 180 + 4)、0日なので日の部分は省略
    assert seconds_to_hms(7384) == "2時間3分4秒"


def test_seconds_to_hms_zero():
    assert seconds_to_hms(0) == "0時間0分0秒"


def test_seconds_to_hms_only_seconds():
    assert seconds_to_hms(45) == "0時間0分45秒"


def test_seconds_to_hms_multiple_days():
    # 2日と少し: 2*86400 + 3661 = 176461秒 -> 2日1時間1分1秒
    assert seconds_to_hms(176461) == "2日1時間1分1秒"


def test_seconds_to_hms_returns_str():
    assert isinstance(seconds_to_hms(100), str)

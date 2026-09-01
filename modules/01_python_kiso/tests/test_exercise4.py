"""演習4のテスト: メモリ使用率のアラートメッセージ生成"""

from exercises.exercise4 import memory_alert_message


def test_memory_alert_message_warning():
    # 7200 / 8000 * 100 = 90.0 -> 閾値80.0を超えるので警告
    assert memory_alert_message(7200, 8000) == "警告: メモリ使用率が90.00%です"


def test_memory_alert_message_normal():
    # 4000 / 8000 * 100 = 50.0 -> 閾値80.0以下なので正常
    assert memory_alert_message(4000, 8000) == "正常: メモリ使用率は50.00%です"


def test_memory_alert_message_custom_threshold():
    # 4800 / 8000 * 100 = 60.0 -> 閾値60.0ちょうどなので正常(超えていない)
    assert (
        memory_alert_message(4800, 8000, threshold_percent=60.0)
        == "正常: メモリ使用率は60.00%です"
    )


def test_memory_alert_message_custom_threshold_warning():
    # 4900 / 8000 * 100 = 61.25 -> 閾値60.0を超えるので警告
    assert (
        memory_alert_message(4900, 8000, threshold_percent=60.0)
        == "警告: メモリ使用率が61.25%です"
    )


def test_memory_alert_message_zero_total():
    # total_mb が 0 のときはゼロ除算を避けて 0.0% とみなす(正常扱い)
    assert memory_alert_message(100, 0) == "正常: メモリ使用率は0.00%です"


def test_memory_alert_message_returns_str():
    assert isinstance(memory_alert_message(100, 1000), str)

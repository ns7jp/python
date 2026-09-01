"""演習4のテスト: retry_with_logging"""
from unittest.mock import Mock

import pytest

from exercises.exercise4 import retry_with_logging


def test_retry_succeeds_on_first_attempt():
    logger = Mock()
    func = Mock(return_value="ok")

    result = retry_with_logging(func, max_attempts=3, logger=logger)

    assert result == "ok"
    assert func.call_count == 1
    logger.warning.assert_not_called()


def test_retry_succeeds_after_some_failures():
    logger = Mock()
    call_count = {"n": 0}

    def flaky():
        call_count["n"] += 1
        if call_count["n"] < 3:
            raise ValueError("一時的な失敗")
        return "成功"

    result = retry_with_logging(flaky, max_attempts=5, logger=logger)

    assert result == "成功"
    assert call_count["n"] == 3
    # 1回目・2回目の失敗の分だけwarningが呼ばれているはず
    assert logger.warning.call_count == 2


def test_retry_all_attempts_fail_raises_last_exception():
    logger = Mock()

    def always_fail():
        raise ValueError("いつも失敗する")

    with pytest.raises(ValueError, match="いつも失敗する"):
        retry_with_logging(always_fail, max_attempts=3, logger=logger)

    assert logger.warning.call_count == 3


def test_retry_logs_attempt_number_in_message():
    logger = Mock()

    def always_fail():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        retry_with_logging(always_fail, max_attempts=2, logger=logger)

    # 1回目・2回目、それぞれの試行回数がメッセージに含まれているか確認する
    logged_messages = [call.args[0] for call in logger.warning.call_args_list]
    assert any("1" in msg for msg in logged_messages)
    assert any("2" in msg for msg in logged_messages)

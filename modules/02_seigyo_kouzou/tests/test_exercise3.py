"""演習3(retry_connection)のテスト。"""
from exercises.exercise3 import retry_connection


def test_success_on_first_try():
    assert retry_connection(3, [True]) == "接続成功(1回目)"


def test_success_on_third_try():
    assert retry_connection(5, [False, False, True, False]) == "接続成功(3回目)"


def test_failure_after_max_retries():
    # max_retries=3回試すが、4回目でしか成功しない設定
    assert retry_connection(3, [False, False, False, True]) == "接続失敗: リトライ上限到達"


def test_failure_when_sequence_runs_out():
    # 試行データが2つしかないのに5回試そうとする
    assert retry_connection(5, [False, False]) == "接続失敗: リトライ上限到達"


def test_zero_max_retries():
    assert retry_connection(0, [True]) == "接続失敗: リトライ上限到達"


def test_all_failures_within_sequence():
    assert retry_connection(3, [False, False, False]) == "接続失敗: リトライ上限到達"

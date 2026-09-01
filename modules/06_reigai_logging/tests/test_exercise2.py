"""演習2のテスト: ServerUnreachableError, check_server, check_server_safe"""
import pytest

from exercises.exercise2 import (
    ServerUnreachableError,
    check_server,
    check_server_safe,
)


def test_check_server_reachable_returns_message():
    assert check_server(True, "web01") == "サーバーweb01: 到達可能"


def test_check_server_unreachable_raises_custom_error():
    with pytest.raises(ServerUnreachableError):
        check_server(False, "web01")


def test_server_unreachable_error_is_exception_subclass():
    assert issubclass(ServerUnreachableError, Exception)


def test_check_server_safe_returns_message_on_success():
    assert check_server_safe(True, "db01") == "サーバーdb01: 到達可能"


def test_check_server_safe_returns_error_message_on_failure():
    assert check_server_safe(False, "db01") == "エラー: サーバーdb01: 到達できません"


def test_check_server_safe_does_not_raise():
    # 例外が外に伝播せず、必ず文字列が返ってくることを確認する
    result = check_server_safe(False, "app01")
    assert isinstance(result, str)

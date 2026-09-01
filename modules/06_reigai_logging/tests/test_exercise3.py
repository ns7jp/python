"""演習3のテスト: setup_logger"""
import logging

import pytest

from exercises.exercise3 import setup_logger


def _cleanup_logger(logger):
    """テスト間でロガーの状態が引き継がれないよう、ハンドラを片付ける。

    logging.getLogger(name) は同じ名前なら同じオブジェクトを返す
    (プロセス内でキャッシュされる)ため、テストごとに使い捨てにできない。
    そこで、各テストの最後にハンドラを閉じて取り除いておく。
    """
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)


@pytest.fixture
def log_path(tmp_path):
    return str(tmp_path / "server_monitor.log")


def test_setup_logger_returns_logger_instance(log_path):
    logger = setup_logger(log_path, "test_logger_instance")
    try:
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger_instance"
    finally:
        _cleanup_logger(logger)


def test_setup_logger_writes_message_to_file(log_path):
    logger = setup_logger(log_path, "test_logger_write")
    try:
        logger.info("サーバー監視を開始しました")
        for handler in logger.handlers:
            handler.flush()

        with open(log_path, encoding="utf-8") as f:
            content = f.read()

        assert "サーバー監視を開始しました" in content
        assert "INFO" in content
    finally:
        _cleanup_logger(logger)


def test_setup_logger_does_not_duplicate_handlers(log_path):
    logger1 = setup_logger(log_path, "test_logger_dedup")
    try:
        first_handler_count = len(logger1.handlers)

        # 同じlogger_nameで再度呼び出しても、同じロガーオブジェクトが返り、
        # ハンドラの数は増えないはず。
        logger2 = setup_logger(log_path, "test_logger_dedup")

        assert logger1 is logger2
        assert first_handler_count == 1
        assert len(logger2.handlers) == 1

        logger2.info("重複確認メッセージ")
        for handler in logger2.handlers:
            handler.flush()

        with open(log_path, encoding="utf-8") as f:
            lines = f.readlines()

        # ハンドラが重複していれば同じメッセージが2行以上出力されてしまう
        matching_lines = [line for line in lines if "重複確認メッセージ" in line]
        assert len(matching_lines) == 1
    finally:
        _cleanup_logger(logger1)


def test_setup_logger_level_is_info_or_lower(log_path):
    logger = setup_logger(log_path, "test_logger_level")
    try:
        assert logger.level <= logging.INFO
        assert logger.handlers[0].level <= logging.INFO
    finally:
        _cleanup_logger(logger)


def test_setup_logger_default_logger_name(log_path):
    logger = setup_logger(log_path)
    try:
        assert logger.name == "server_monitor"
    finally:
        _cleanup_logger(logger)

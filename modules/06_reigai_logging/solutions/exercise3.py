"""演習3の模範解答: loggingモジュールで、ファイルに記録を残すロガーを組み立てる

仕様の詳細はexercises/exercise3.pyのdocstringを参照してください。
"""
import logging


def setup_logger(log_file_path, logger_name="server_monitor"):
    """log_file_pathにログを出力するロガーを作成して返す。

    仕様はexercises/exercise3.pyのdocstringを参照。
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # 既にハンドラが設定済みなら、重複して追加しない。
    if not logger.handlers:
        handler = logging.FileHandler(log_file_path, encoding="utf-8")
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger

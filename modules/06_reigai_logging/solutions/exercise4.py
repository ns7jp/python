"""演習4の模範解答: 例外処理とロギングを組み合わせて「リトライ処理」を作る

仕様の詳細はexercises/exercise4.pyのdocstringを参照してください。
"""


def retry_with_logging(func, max_attempts, logger):
    """funcを最大max_attempts回呼び出し、失敗のたびにログを記録する。

    仕様はexercises/exercise4.pyのdocstringを参照。
    """
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as exc:
            logger.warning(f"{attempt}回目の試行が失敗しました: {exc}")
            last_error = exc

    raise last_error

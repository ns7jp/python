"""演習4(応用): 例外処理とロギングを組み合わせて「リトライ処理」を作る

サーバー運用では、一時的な不調(ネットワークの瞬断など)が原因で
処理が失敗しても、すぐに諦めずに何度か再挑戦(リトライ)したい場面が
多くあります。この演習では、これまで学んだ「例外処理」と「ロギング」を
組み合わせ、失敗のたびにログを記録しながら再挑戦する
retry_with_logging 関数を実装します。
"""


def retry_with_logging(func, max_attempts, logger):
    """funcを最大max_attempts回呼び出し、失敗のたびにログを記録する。

    引数なし(func()の形)で呼び出せる関数funcを、最大でmax_attempts回
    実行を試みる。

    - funcの呼び出しが成功した(例外が発生しなかった)場合、その場で
      戻り値を返す(それ以上リトライしない)。
    - funcの呼び出しで例外が発生した場合は、logger.warning(...)を使い、
      「何回目の試行が失敗したか」と「発生した例外の内容」をログに
      記録したうえで、次の試行に進む(プログラムを止めない)。
    - max_attempts回すべて失敗した場合は、最後に発生した例外を
      改めてraiseする(呼び出し元に「結局だめだった」ことを伝える)。

    引数:
        func (Callable[[], Any]): 引数なしで呼び出せる処理。
        max_attempts (int): 最大試行回数(1以上)。
        logger (logging.Logger): 失敗時にwarningを記録するロガー。

    戻り値:
        Any: funcの呼び出しが成功したときの戻り値。

    例外:
        funcが送出した例外のうち、最後(max_attempts回目)に発生した
        ものをそのままraiseする(max_attempts回すべて失敗した場合)。

    入出力例:
        >>> import logging
        >>> logger = logging.getLogger("retry_example")
        >>> calls = {"count": 0}
        >>> def flaky():
        ...     calls["count"] += 1
        ...     if calls["count"] < 3:
        ...         raise ValueError("一時的な失敗")
        ...     return "成功"
        >>> retry_with_logging(flaky, max_attempts=5, logger=logger)
        '成功'
        (1回目・2回目の失敗がlogger.warningで記録され、3回目で成功する)

        >>> def always_fail():
        ...     raise ValueError("いつも失敗する")
        >>> retry_with_logging(always_fail, max_attempts=3, logger=logger)
        (3回とも失敗を記録した後、最後にValueErrorがraiseされる)
    """
    # TODO: 以下の手順で実装してください。
    #   1. 最後に発生した例外を覚えておく変数(例: last_error = None)を用意する
    #   2. for attempt in range(1, max_attempts + 1): でループする
    #      - try節で func() を呼び出し、成功したらその戻り値をそのままreturnする
    #      - except Exception as exc: の節で、
    #        logger.warning(f"{attempt}回目の試行が失敗しました: {exc}") の
    #        ようにログを記録し、last_error に exc を保存する
    #   3. ループがすべて失敗で終わった場合、raise last_error で
    #      最後の例外を改めてraiseする
    raise NotImplementedError("retry_with_logging を実装してください")

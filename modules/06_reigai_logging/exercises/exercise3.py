"""演習3: loggingモジュールで、ファイルに記録を残すロガーを組み立てる

print() は実行中の画面に表示されるだけですが、サーバー運用の現場では
「いつ・何が起きたか」を後から追跡できるよう、ログをファイルに残す
ことがほぼ必須です。この演習では、Python標準の logging モジュールを
使って、ログをファイルに出力するロガー(logger)を組み立てる関数を
実装します。
"""
import logging


def setup_logger(log_file_path, logger_name="server_monitor"):
    """log_file_pathにログを出力するロガーを作成して返す。

    logging.getLogger(logger_name) でロガー(記録係)を取得し、
    以下の設定を行う。

    - ロガー自体のレベルを logging.INFO 以上にする
      (これより低いレベル、例えばDEBUGは記録されない)
    - log_file_path にログを書き出す logging.FileHandler を作成し、
      レベルを logging.INFO 以上にする
    - ログの書式(フォーマット)を logging.Formatter で設定する
      (例: 時刻・レベル名・メッセージを含む書式)
    - 作成したFileHandlerをロガーに addHandler() で追加する

    (重要) logging.getLogger(logger_name) は、同じ名前で呼び出すと
    "同じロガーオブジェクト" を返す仕組みになっている。そのため、
    この関数を同じ logger_name で複数回呼び出すと、何も対策しなければ
    FileHandlerが毎回追加されてしまい、1件のログメッセージが
    2回、3回...と重複して記録されてしまう。これを防ぐため、
    「ロガーに既にハンドラが設定済みかどうか」を確認し、
    設定済みであれば新しいハンドラを追加しない、という配慮が必要になる。

    引数:
        log_file_path (str): ログファイルの出力先パス。
        logger_name (str): ロガーの名前。省略時は "server_monitor"。

    戻り値:
        logging.Logger: 設定済みのロガーオブジェクト。

    入出力例:
        >>> logger = setup_logger("/tmp/example.log", "my_logger")
        >>> logger.info("サーバー監視を開始しました")
        (/tmp/example.log に、時刻付きでこのメッセージが書き込まれる)
        >>> logger2 = setup_logger("/tmp/example.log", "my_logger")
        >>> logger2 is logger
        True
        >>> len(logger.handlers)
        1
        (同じlogger_nameで再度呼び出しても、ハンドラは1個のまま)
    """
    # TODO: 以下の手順で実装してください。
    #   1. logger = logging.getLogger(logger_name) でロガーを取得する
    #   2. logger.setLevel(logging.INFO) でロガーのレベルを設定する
    #   3. if not logger.handlers: (まだハンドラが1つもなければ)
    #        - logging.FileHandler(log_file_path) を作成する
    #        - handler.setLevel(logging.INFO) を設定する
    #        - logging.Formatter(...) でフォーマットを作り、
    #          handler.setFormatter(...) に渡す
    #        - logger.addHandler(handler) でロガーに追加する
    #   4. logger を返す
    raise NotImplementedError("setup_logger を実装してください")

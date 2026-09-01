"""総合演習: ミニ・サーバー監視ツール (monitor.py)

この章は、これまでの章で学んできた次の内容を組み合わせて作る
「集大成」のミニプロジェクトです。

- 03章(データ構造): 辞書・リストを使った設定・結果の表現
- 04章(関数・モジュール): 役割ごとに小さな関数に分けて組み合わせる設計
- 05章(ファイル・OS操作): 設定ファイルの読み込み
- 06章(例外処理とロギング): try/exceptによる安全な実装、
  loggingモジュールでの記録(setup_loggerを流用してよい)
- 08章(ネットワーク/API): socketによるポート疎通確認、requestsに
  よるHTTP確認、依存性注入(http_get引数)によるテストしやすい設計
- 09章(設定ファイル管理): JSON設定ファイルの読み込みと活用
- 10章(テストの基本): pytestによる自動テスト

この章では、複数のサーバー(監視対象)に対して
「TCPポートは開いているか」「HTTPで200番台の応答が返るか」を
チェックし、連続して失敗している対象があればアラートとして
報告する、ミニ・サーバー監視ツールを組み立てます。

仕様の詳細は各関数のdocstringを参照してください。
"""
import json
import socket

import requests


def load_config(config_path):
    """JSON形式の設定ファイルを読み込み、辞書(dict)として返す。

    sample_config.jsonのような形式のJSONファイルを想定している。

    引数:
        config_path (str): 読み込むJSON設定ファイルのパス。

    戻り値:
        dict: JSONファイルの内容をそのままPythonの辞書として返す。

    入出力例:
        >>> load_config("modules/11_capstone_server_monitor/sample_config.json")
        {'targets': [...], 'alert_threshold_consecutive_failures': 3}
    """
    # TODO: 以下の手順で実装してください。
    #   1. open(config_path, "r", encoding="utf-8") でファイルを開く
    #   2. json.load(f) でJSONを読み込み、辞書として返す
    #      (09章のload_json_configを参考にしてよい)
    raise NotImplementedError("load_config を実装してください")


def check_target_port(host, port, timeout=1.0):
    """指定したhost:portへTCP接続を試み、接続できるかどうかを調べる。

    08章のis_port_openと同様の考え方(socket.create_connectionを
    try/exceptで包む)で実装する。

    引数:
        host (str): 接続先ホスト名またはIPアドレス。
        port (int): 接続先ポート番号。
        timeout (float): 接続を待つ最大秒数(デフォルト1.0秒)。

    戻り値:
        bool: 接続に成功すればTrue、失敗すればFalse。

    入出力例:
        >>> check_target_port("127.0.0.1", 65000)  # 何も待ち受けていない場合
        False
    """
    # TODO: 以下の手順で実装してください。
    #   1. try節で socket.create_connection((host, port), timeout=timeout)
    #      を with 文と組み合わせて呼び出す
    #   2. 成功したら True を返す
    #   3. except OSError: の節で False を返す
    #      (ConnectionRefusedErrorやsocket.timeoutもOSErrorの派生なので
    #       まとめて捕まえられる)
    raise NotImplementedError("check_target_port を実装してください")


def check_target_http(http_url, http_get=None):
    """http_urlに対してHTTP GETリクエストを送り、正常応答かどうかを調べる。

    08章で学んだ「依存性注入」の考え方を使う。http_get引数に
    ダミー関数を渡せば、実際のネットワーク通信なしにテストできる。

    引数:
        http_url (str または None): チェック対象のURL。Noneまたは
            空文字列の場合は「HTTPチェックの対象外」を意味する。
        http_get (Callable または None): GETリクエストを送る関数。
            Noneの場合はrequests.getを使う。
            (関数はurlを受け取り、.status_code属性を持つ
            オブジェクトを返すことを想定している)

    戻り値:
        bool または None:
            - http_urlがNoneまたは空文字列なら None
              (チェック対象外という意味)
            - リクエストが成功し、ステータスコードが200番台なら True
            - リクエストが成功したが200番台以外の場合、または
              リクエスト中に例外が発生した場合は False

    入出力例:
        >>> check_target_http(None)
        None
        >>> check_target_http("")
        None
        >>> class FakeResponse:
        ...     status_code = 200
        >>> check_target_http("http://example.com", http_get=lambda url: FakeResponse())
        True
    """
    # TODO: 以下の手順で実装してください。
    #   1. http_urlがNoneまたは空文字列(falsyな値)なら None を返す
    #   2. getter = http_get if http_get is not None else requests.get
    #      のように、使用するGET関数を決める
    #   3. try節でgetter(http_url)を呼び出し、レスポンスの
    #      status_codeが200以上300未満なら True、そうでなければ False
    #      を返す
    #   4. except Exception: の節で False を返す
    #      (通信エラー・タイムアウトなどをまとめて捕まえる)
    raise NotImplementedError("check_target_http を実装してください")


def check_target(target, http_get=None):
    """1つの監視対象(target)について、ポートとHTTPの両方をチェックする。

    check_target_portとcheck_target_httpを組み合わせて使う。

    引数:
        target (dict): "name", "host", "port", "http_url" キーを
            含む辞書(sample_config.jsonの"targets"の要素1つ分)。
        http_get (Callable または None): check_target_httpに
            そのまま渡すダミーGET関数(テスト用)。

    戻り値:
        dict: 次の形式の辞書。
            {
                "name": str,          # targetの名前
                "port_ok": bool,      # ポート疎通確認の結果
                "http_ok": bool または None,  # HTTPチェックの結果
                "healthy": bool,      # 総合的に正常とみなせるか
            }
            healthyは、port_okがTrueであり、かつhttp_okがFalseで
            ない(True または None)ときに True とする。

    入出力例:
        >>> target = {"name": "web-01", "host": "127.0.0.1",
        ...           "port": 65000, "http_url": None}
        >>> check_target(target)
        {'name': 'web-01', 'port_ok': False, 'http_ok': None, 'healthy': False}
    """
    # TODO: 以下の手順で実装してください。
    #   1. check_target_port(target["host"], target["port"]) を呼び、
    #      port_ok に結果を入れる
    #   2. check_target_http(target["http_url"], http_get=http_get) を
    #      呼び、http_ok に結果を入れる
    #   3. healthy = port_ok and (http_ok is not False) を計算する
    #      (http_okがTrueでもNoneでも、Falseでなければ良しとする)
    #   4. {"name": target["name"], "port_ok": port_ok,
    #       "http_ok": http_ok, "healthy": healthy} を返す
    raise NotImplementedError("check_target を実装してください")


def run_monitor_cycle(config, http_get=None):
    """設定内のすべての監視対象について、1回分のチェックを実行する。

    引数:
        config (dict): load_configで読み込んだ設定辞書
            ("targets"キーにtargetのリストを持つ)。
        http_get (Callable または None): 各targetのcheck_targetに
            そのまま渡すダミーGET関数(テスト用)。

    戻り値:
        list[dict]: config["targets"]の各要素についてcheck_targetを
            実行した結果のリスト(順番はconfig["targets"]と同じ)。

    入出力例:
        >>> config = {"targets": [
        ...     {"name": "web-01", "host": "127.0.0.1", "port": 65000,
        ...      "http_url": None},
        ... ]}
        >>> run_monitor_cycle(config)
        [{'name': 'web-01', 'port_ok': False, 'http_ok': None, 'healthy': False}]
    """
    # TODO: 以下の手順で実装してください。
    #   1. 結果を入れる空リストを用意する
    #   2. for target in config["targets"]: でループし、
    #      check_target(target, http_get=http_get) の結果をリストに追加する
    #   3. 完成したリストを返す
    raise NotImplementedError("run_monitor_cycle を実装してください")


def update_failure_counts(results, failure_counts):
    """監視結果をもとに、連続失敗回数の辞書を更新する。

    healthyがFalseだったtargetは連続失敗回数を1増やし、healthyが
    Trueだったtargetは連続失敗回数を0にリセットする。

    引数:
        results (list[dict]): run_monitor_cycleが返す結果のリスト
            (各要素は"name"と"healthy"キーを持つ)。
        failure_counts (dict): これまでの連続失敗回数を表す辞書
            ({target名: 連続失敗回数})。まだ登場していないtarget名は
            キーが存在しないものとして扱ってよい。

    戻り値:
        dict: 更新後の新しい連続失敗回数の辞書。
            引数のfailure_counts自体は書き換えず、新しい辞書を
            作って返すこと。

    入出力例:
        >>> results = [
        ...     {"name": "web-01", "healthy": False},
        ...     {"name": "app-01", "healthy": True},
        ... ]
        >>> update_failure_counts(results, {"web-01": 2, "app-01": 5})
        {'web-01': 3, 'app-01': 0}
        >>> update_failure_counts(results, {})
        {'web-01': 1, 'app-01': 0}
    """
    # TODO: 以下の手順で実装してください。
    #   1. 引数のfailure_countsをコピーして新しい辞書を作る
    #      (例: new_counts = dict(failure_counts))
    #   2. for result in results: でループする
    #      - healthyがFalseなら、その名前の現在の値
    #        (new_counts.get(name, 0))に1を足して入れ直す
    #      - healthyがTrueなら、その名前の値を0にする
    #   3. 新しい辞書を返す
    raise NotImplementedError("update_failure_counts を実装してください")


def get_alerts(failure_counts, threshold):
    """連続失敗回数がthreshold以上のtarget名の一覧を返す。

    引数:
        failure_counts (dict): {target名: 連続失敗回数} の辞書
            (update_failure_countsが返す形式)。
        threshold (int): アラートを出す基準となる連続失敗回数。

    戻り値:
        list[str]: 連続失敗回数がthreshold以上のtarget名のリスト。

    入出力例:
        >>> get_alerts({"web-01": 3, "app-01": 1}, threshold=3)
        ['web-01']
        >>> get_alerts({"web-01": 1, "app-01": 2}, threshold=3)
        []
    """
    # TODO: 以下の手順で実装してください。
    #   1. failure_counts.items() でループし、
    #      count >= threshold となる name をリストに集める
    #   2. そのリストを返す(リスト内包表記を使うと簡潔に書ける)
    raise NotImplementedError("get_alerts を実装してください")


def log_cycle_result(logger, results):
    """1回分の監視結果を、loggerを使って記録する。

    06章のsetup_logger(exercises/solutions両方の06章を参照)で
    作成したロガーをそのまま渡して使うことができる。

    引数:
        logger (logging.Logger): ログを記録するためのロガー。
        results (list[dict]): run_monitor_cycleが返す結果のリスト。

    戻り値:
        None: この関数は値を返さず、ログを記録するだけでよい。

    入出力例:
        >>> import logging
        >>> logger = logging.getLogger("example")
        >>> results = [{"name": "web-01", "port_ok": True,
        ...             "http_ok": None, "healthy": True}]
        >>> log_cycle_result(logger, results)
        (logger.infoで「web-01は正常です」といった内容が記録される)
    """
    # TODO: 以下の手順で実装してください。
    #   1. for result in results: でループする
    #   2. result["healthy"]がTrueならlogger.info(...)で、
    #      Falseならlogger.warning(...)で、resultの内容
    #      (name, port_ok, http_okなど)をメッセージに含めて記録する
    raise NotImplementedError("log_cycle_result を実装してください")


if __name__ == "__main__":
    # このブロックはCLI(コマンドラインツール)として monitor.py を
    # 直接実行したときだけ動く部分で、テストの対象ではない。
    #
    # sample_config.jsonを読み込み、1回分の監視サイクルを実行し、
    # 結果をログに出力し、アラート対象があれば表示する、という
    # 一連の流れを体験できるようにしてある。
    #
    # 実行方法:
    #   cd /home/user/python
    #   python3 modules/11_capstone_server_monitor/exercises/monitor.py
    import logging
    import os

    def setup_logger(log_file_path, logger_name="server_monitor"):
        # 06章のsetup_logger相当のロガー組み立て処理
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.FileHandler(log_file_path, encoding="utf-8")
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    this_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(os.path.dirname(this_dir), "sample_config.json")
    log_path = os.path.join(this_dir, "monitor.log")

    config = load_config(config_path)
    logger = setup_logger(log_path)

    results = run_monitor_cycle(config)
    log_cycle_result(logger, results)

    failure_counts = update_failure_counts(results, {})
    threshold = config.get("alert_threshold_consecutive_failures", 3)
    alerts = get_alerts(failure_counts, threshold)

    print("監視結果:", results)
    if alerts:
        print("アラート対象:", alerts)
    else:
        print("アラート対象はありません。")

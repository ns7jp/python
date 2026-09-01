"""総合演習の模範解答: ミニ・サーバー監視ツール (monitor.py)

仕様の詳細はexercises/monitor.pyの各関数のdocstringを参照してください。
"""
import json
import socket

import requests


def load_config(config_path):
    """JSON形式の設定ファイルを読み込み、辞書(dict)として返す。

    仕様はexercises/monitor.pyのdocstringを参照。
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_target_port(host, port, timeout=1.0):
    """指定したhost:portへTCP接続を試み、接続できるかどうかを調べる。

    仕様はexercises/monitor.pyのdocstringを参照。
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        # ConnectionRefusedError, socket.timeout(TimeoutError) など、
        # 接続に関する例外はすべてOSErrorの派生クラスなのでまとめて捕まえる
        return False


def check_target_http(http_url, http_get=None):
    """http_urlに対してHTTP GETリクエストを送り、正常応答かどうかを調べる。

    仕様はexercises/monitor.pyのdocstringを参照。
    """
    if not http_url:
        return None

    getter = http_get if http_get is not None else requests.get
    try:
        response = getter(http_url)
        return 200 <= response.status_code < 300
    except Exception:
        # タイムアウト・接続エラーなど、通信中に起こりうる様々な例外を
        # まとめて捕まえ、呼び出し元にはFalseとして伝える
        return False


def check_target(target, http_get=None):
    """1つの監視対象(target)について、ポートとHTTPの両方をチェックする。

    仕様はexercises/monitor.pyのdocstringを参照。
    """
    port_ok = check_target_port(target["host"], target["port"])
    http_ok = check_target_http(target.get("http_url"), http_get=http_get)
    healthy = bool(port_ok) and (http_ok is not False)

    return {
        "name": target["name"],
        "port_ok": port_ok,
        "http_ok": http_ok,
        "healthy": healthy,
    }


def run_monitor_cycle(config, http_get=None):
    """設定内のすべての監視対象について、1回分のチェックを実行する。

    仕様はexercises/monitor.pyのdocstringを参照。
    """
    results = []
    for target in config["targets"]:
        results.append(check_target(target, http_get=http_get))
    return results


def update_failure_counts(results, failure_counts):
    """監視結果をもとに、連続失敗回数の辞書を更新する。

    仕様はexercises/monitor.pyのdocstringを参照。
    """
    new_counts = dict(failure_counts)

    for result in results:
        name = result["name"]
        if result["healthy"]:
            new_counts[name] = 0
        else:
            new_counts[name] = new_counts.get(name, 0) + 1

    return new_counts


def get_alerts(failure_counts, threshold):
    """連続失敗回数がthreshold以上のtarget名の一覧を返す。

    仕様はexercises/monitor.pyのdocstringを参照。
    """
    return [name for name, count in failure_counts.items() if count >= threshold]


def log_cycle_result(logger, results):
    """1回分の監視結果を、loggerを使って記録する。

    仕様はexercises/monitor.pyのdocstringを参照。
    06章のsetup_loggerで作成したロガーをそのまま渡して使える。
    """
    for result in results:
        message = (
            f"{result['name']}: port_ok={result['port_ok']}, "
            f"http_ok={result['http_ok']}, healthy={result['healthy']}"
        )
        if result["healthy"]:
            logger.info(message)
        else:
            logger.warning(message)


if __name__ == "__main__":
    # このブロックはCLI(コマンドラインツール)として monitor.py を
    # 直接実行したときだけ動く部分で、テストの対象ではない。
    #
    # 実行方法:
    #   cd /home/user/python
    #   python3 modules/11_capstone_server_monitor/solutions/monitor.py
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

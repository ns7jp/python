"""
第11章(総合演習): ミニ・サーバー監視ツール - サンプルコード

この章はこれまでの章の集大成です。このサンプルでは、次の内容を
組み合わせた「ミニ・サーバー監視ツール」がどう動くのかを、
実際に手を動かしながら確認します。

    1. JSON設定ファイルの読み込み(05章・09章)
    2. socketによるTCPポート疎通確認(08章)
    3. requests(に見立てたダミー関数)によるHTTPチェックと
       依存性注入(08章)
    4. loggingモジュールによる監視結果の記録(06章)
    5. 連続失敗回数のカウントとアラート判定(03章・04章)
    6. 複数回の監視サイクルをループで回す統合フロー

(重要) このサンプルは実在の外部ホスト・外部インターネットには一切
接続しません。ポート確認は127.0.0.1(自分自身のマシン)上で一時的に
立てたソケットサーバーに対して行い、HTTP通信の部分はすべてダミー
関数に置き換えています。

実行方法:
    cd /home/user/python
    python3 modules/11_capstone_server_monitor/examples/example.py

(注意) exercises/monitor.py、solutions/monitor.py にも同じ関数群が
定義されていますが、この examples/example.py は他の章と同様に、
それらに依存せず単体で読んで実行できるように作られています。
"""
import json
import logging
import os
import socket
import tempfile
import threading


# ---------------------------------------------------------------------------
# 1. JSON設定ファイルの読み込み
# ---------------------------------------------------------------------------
def load_config(config_path):
    """JSON形式の設定ファイルを読み込み、辞書として返す(09章の復習)。"""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 2. TCPポート疎通確認
# ---------------------------------------------------------------------------
def check_target_port(host, port, timeout=1.0):
    """指定したhost:portへTCP接続を試み、成功すればTrue、失敗すればFalse。

    08章のis_port_openと同じ考え方。ConnectionRefusedErrorや
    socket.timeoutはすべてOSErrorの派生クラスなのでまとめて捕まえる。
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# 3. HTTPチェック(依存性注入によるダミー化)
# ---------------------------------------------------------------------------
def check_target_http(http_url, http_get):
    """http_urlに対してGETリクエストを送り、200番台の応答かどうかを調べる。

    08章の「依存性注入」の考え方をそのまま使う。本物のrequests.getの
    代わりに、このサンプルでは常にダミー関数(http_get)を渡すため、
    外部への通信は一切発生しない。
    """
    if not http_url:
        return None
    try:
        response = http_get(http_url)
        return 200 <= response.status_code < 300
    except Exception:
        return False


def check_target(target, http_get):
    """1つの監視対象について、ポートとHTTPの両方をチェックする。"""
    port_ok = check_target_port(target["host"], target["port"])
    http_ok = check_target_http(target.get("http_url"), http_get)
    healthy = bool(port_ok) and (http_ok is not False)
    return {
        "name": target["name"],
        "port_ok": port_ok,
        "http_ok": http_ok,
        "healthy": healthy,
    }


def run_monitor_cycle(config, http_get):
    """設定内のすべての監視対象について、1回分のチェックを実行する。"""
    return [check_target(target, http_get) for target in config["targets"]]


# ---------------------------------------------------------------------------
# 4. loggingによる記録
# ---------------------------------------------------------------------------
def build_demo_logger(log_file_path):
    """06章のsetup_loggerと同じ考え方でロガーを組み立てる。"""
    logger = logging.getLogger("example_capstone_monitor")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def log_cycle_result(logger, results):
    """監視結果を、healthyに応じてinfo/warningで記録する。"""
    for result in results:
        message = (
            f"{result['name']}: port_ok={result['port_ok']}, "
            f"http_ok={result['http_ok']}, healthy={result['healthy']}"
        )
        if result["healthy"]:
            logger.info(message)
        else:
            logger.warning(message)


# ---------------------------------------------------------------------------
# 5. 連続失敗回数のカウントとアラート判定
# ---------------------------------------------------------------------------
def update_failure_counts(results, failure_counts):
    """healthyがFalseなら+1、Trueなら0にリセットした新しい辞書を返す。"""
    new_counts = dict(failure_counts)
    for result in results:
        name = result["name"]
        if result["healthy"]:
            new_counts[name] = 0
        else:
            new_counts[name] = new_counts.get(name, 0) + 1
    return new_counts


def get_alerts(failure_counts, threshold):
    """連続失敗回数がthreshold以上のtarget名の一覧を返す。"""
    return [name for name, count in failure_counts.items() if count >= threshold]


# ---------------------------------------------------------------------------
# ダミーのHTTPレスポンス・GET関数(外部通信を一切行わない)
# ---------------------------------------------------------------------------
class FakeResponse:
    """requestsのResponseもどきの、ステータスコードだけ持つダミークラス。"""

    def __init__(self, status_code):
        self.status_code = status_code


def make_fake_http_get(status_code):
    """常に指定したステータスコードを返すダミーのGET関数を作る。"""

    def fake_get(url):
        return FakeResponse(status_code)

    return fake_get


def main():
    print("=" * 60)
    print("1. JSON設定ファイルの読み込み")
    print("=" * 60)
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "sample_config.json",
    )
    config = load_config(config_path)
    print(f"  読み込んだ設定: {config}")

    print()
    print("=" * 60)
    print("2. 監視対象を模したローカルサーバーを準備する")
    print("=" * 60)
    # web-01役: 実際にlistenする(正常なサーバーを模す)
    web_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    web_server.bind(("127.0.0.1", 0))
    web_port = web_server.getsockname()[1]
    web_server.listen(1)

    def accept_loop(server_socket):
        # サンプルなので接続を受けてすぐ閉じるだけの簡易処理
        while True:
            try:
                conn, _addr = server_socket.accept()
            except OSError:
                break
            conn.close()

    thread = threading.Thread(target=accept_loop, args=(web_server,), daemon=True)
    thread.start()

    # app-01役: bindだけしてすぐ閉じ、「落ちているサーバー」を模す
    app_socket_for_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app_socket_for_port.bind(("127.0.0.1", 0))
    app_port = app_socket_for_port.getsockname()[1]
    app_socket_for_port.close()  # listenせずに閉じる -> 接続は拒否される

    demo_config = {
        "targets": [
            {
                "name": "web-01",
                "host": "127.0.0.1",
                "port": web_port,
                "http_url": "http://127.0.0.1/health",
            },
            {
                "name": "app-01",
                "host": "127.0.0.1",
                "port": app_port,
                "http_url": None,
            },
        ],
        "alert_threshold_consecutive_failures": 3,
    }
    print(f"  web-01(正常役) -> ポート {web_port} で待ち受け中")
    print(f"  app-01(異常役) -> ポート {app_port} は何も待ち受けていない")

    print()
    print("=" * 60)
    print("3〜5. 複数回の監視サイクルを回し、連続失敗回数とアラートを追跡する")
    print("=" * 60)
    log_path = os.path.join(tempfile.gettempdir(), "python_kiso_11_example.log")
    logger = build_demo_logger(log_path)

    fake_http_get = make_fake_http_get(200)  # web-01のHTTPチェックは常に200を返す
    failure_counts = {}

    for cycle in range(1, 4):
        print(f"\n  --- 監視サイクル {cycle}回目 ---")
        results = run_monitor_cycle(demo_config, fake_http_get)
        for r in results:
            print(f"    {r}")

        log_cycle_result(logger, results)
        failure_counts = update_failure_counts(results, failure_counts)
        print(f"    連続失敗回数: {failure_counts}")

        alerts = get_alerts(
            failure_counts, demo_config["alert_threshold_consecutive_failures"]
        )
        if alerts:
            print(f"    [アラート] 連続失敗が閾値に達した対象: {alerts}")
        else:
            print("    アラート対象はまだありません")

    # 後片付け
    web_server.close()

    for handler in logger.handlers:
        handler.flush()

    print()
    print("=" * 60)
    print("6. ログファイルの中身を確認する")
    print("=" * 60)
    print(f"  ログファイル: {log_path}")
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            print(f"  {line.rstrip()}")


if __name__ == "__main__":
    main()

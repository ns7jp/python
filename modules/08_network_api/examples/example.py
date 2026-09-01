"""
第8章: ネットワークとAPI連携 - サンプルコード

このサンプルでは、以下のポイントを実際に動かしながら確認します。

    1. socketモジュールの基礎(TCP接続によるポート疎通確認)
    2. requestsライブラリでのHTTP通信と依存性注入
    3. json.loads / json.dumps によるデータのやり取り
    4. unittest.mockを使ったモック(外部通信を行わないテストの考え方)
    5. socketモジュールで作る簡易エコーサーバー

(重要) このサンプルは実在の外部ホスト・外部インターネットには一切
接続しません。ポート確認は127.0.0.1(自分自身のマシン)上で一時的に
立てたソケットサーバーに対して行い、HTTP通信の部分はすべて
ダミー関数やモックに置き換えています。

実行方法:
    cd /home/user/python
    python3 modules/08_network_api/examples/example.py
"""
import json
import socket
import threading
import time
from unittest.mock import patch

import requests


# ---------------------------------------------------------------------------
# 1. socketモジュールの基礎(TCP接続によるポート疎通確認)
# ---------------------------------------------------------------------------
def is_port_open(host, port, timeout=1.0):
    """指定したhost:portへTCP接続を試み、成功すればTrue、失敗すればFalse。

    サーバーの「疎通確認(そつうかくにん)」、つまり「このポートは
    ちゃんと応答するか?」を調べる基本的な方法。SSH(22番)やHTTP
    (80番)など、サーバー運用ではポート単位での死活確認が日常的に
    行われる。
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def demo_port_check():
    # 127.0.0.1上に「空いているポート」を自分で1つ用意する。
    # 固定のポート番号を決め打ちすると、環境によってはすでに
    # 別のプロセスが使っていて失敗することがあるため、
    # bindするポートには0を指定し、OSに自動で選んでもらう。
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 0))
    port = server_socket.getsockname()[1]  # 実際に割り当てられたポート番号
    server_socket.listen(1)

    print(f"  127.0.0.1:{port} でソケットサーバーを起動しました")
    print(f"  is_port_open('127.0.0.1', {port}) -> {is_port_open('127.0.0.1', port)}")

    server_socket.close()
    # サーバーを閉じた直後は、同じポートに接続しようとしても
    # 応答するものがないため接続が拒否される(Connection Refused)
    print(f"  サーバーを閉じました")
    print(f"  is_port_open('127.0.0.1', {port}) -> {is_port_open('127.0.0.1', port)}")


# ---------------------------------------------------------------------------
# 2. requestsライブラリでのHTTP通信と依存性注入
# ---------------------------------------------------------------------------
def check_http_status(url, http_get=None):
    """URLにGETリクエストを送り、HTTPステータスコードを返す。

    http_get引数に関数を渡すと、実際の通信の代わりにその関数が
    使われる(依存性注入)。これにより、テスト時には本物のネットワーク
    通信を行わずに、この関数の「通信に成功した場合」「失敗した場合」の
    振る舞いを確認できる。
    """
    getter = http_get if http_get is not None else requests.get
    try:
        response = getter(url)
        return response.status_code
    except Exception:
        return None


class _FakeMonitoringResponse:
    """requestsのResponseオブジェクトに似せた、デモ用のダミークラス。"""

    def __init__(self, status_code):
        self.status_code = status_code


def demo_http_status_with_dependency_injection():
    # 監視対象のAPIが200(正常)を返すケースを、ダミー関数で再現する
    def fake_get_ok(url):
        print(f"    (本物の通信の代わりにダミー関数が呼ばれました: {url})")
        return _FakeMonitoringResponse(200)

    result_ok = check_http_status("http://monitoring.example.local/health", http_get=fake_get_ok)
    print(f"  正常系: check_http_status(..., http_get=fake_get_ok) -> {result_ok}")

    # 監視対象のAPIが500(サーバーエラー)を返すケースを再現する
    def fake_get_error(url):
        return _FakeMonitoringResponse(500)

    result_error = check_http_status(
        "http://monitoring.example.local/health", http_get=fake_get_error
    )
    print(f"  異常系: check_http_status(..., http_get=fake_get_error) -> {result_error}")

    # 通信自体が失敗する(タイムアウトなど)ケースを再現する
    def fake_get_timeout(url):
        raise TimeoutError("接続がタイムアウトしました(デモ用の疑似エラー)")

    result_timeout = check_http_status(
        "http://monitoring.example.local/health", http_get=fake_get_timeout
    )
    print(f"  タイムアウト系: check_http_status(..., http_get=fake_get_timeout) -> {result_timeout}")


def demo_http_status_with_mock():
    # http_get引数を渡さない場合は requests.get が使われる。
    # unittest.mock.patch を使うと、requests.get そのものを一時的に
    # 差し替えることができ、http_get引数を使わない既存コードに対しても
    # 実際の通信を発生させずにテストできる。
    with patch("requests.get") as mock_get:
        mock_get.return_value = _FakeMonitoringResponse(200)
        result = check_http_status("http://monitoring.example.local/health")
        print(f"  unittest.mock.patchでrequests.getを差し替えた結果 -> {result}")
        print(f"  mock_getが呼ばれた回数: {mock_get.call_count}回")


# ---------------------------------------------------------------------------
# 3. json.loads / json.dumps によるデータのやり取り
# ---------------------------------------------------------------------------
def parse_server_status_json(json_text):
    """JSON文字列から"status", "cpu", "memory"だけを取り出した辞書を返す。

    不正なJSONの場合は空の辞書を返す。
    """
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return {key: data[key] for key in ("status", "cpu", "memory") if key in data}


def demo_json_parsing():
    # json.dumps: Pythonの辞書 -> JSON文字列(APIにデータを送るときなどに使う)
    outgoing = {"host": "web01", "action": "healthcheck"}
    outgoing_json = json.dumps(outgoing, ensure_ascii=False)
    print(f"  json.dumps(outgoing) -> {outgoing_json}")

    # json.loads: JSON文字列 -> Pythonの辞書(APIから返ってきたデータを読むときに使う)
    incoming_json = '{"status": "ok", "cpu": 42, "memory": 70, "hostname": "web01"}'
    parsed = parse_server_status_json(incoming_json)
    print(f"  正常なJSON: parse_server_status_json(...) -> {parsed}")

    broken_json = "これはJSONとして壊れた文字列です"
    parsed_broken = parse_server_status_json(broken_json)
    print(f"  壊れたJSON: parse_server_status_json(...) -> {parsed_broken}")


# ---------------------------------------------------------------------------
# 4. socketモジュールで作る簡易エコーサーバー
# ---------------------------------------------------------------------------
def start_echo_server(host, port):
    """host:portで1接続分だけ受け付け、受信データをそのまま送り返す。

    ブロッキングする作りのため、呼び出し側はthreading.Threadに乗せて
    daemon=Trueで起動することを想定している。
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        conn, _addr = server_socket.accept()
        try:
            data = conn.recv(4096)
            if data:
                conn.sendall(data)
        finally:
            conn.close()
    finally:
        server_socket.close()


def send_echo_message(host, port, message, timeout=2.0):
    """host:portに接続し、messageを送信して応答を文字列で受け取る。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.sendall(message.encode("utf-8"))
        data = sock.recv(4096)
    return data.decode("utf-8")


def demo_echo_server():
    # まず空いているポートを1つ確保してから、そのポート番号を使って
    # エコーサーバーを立てる(ポートの決め打ちを避けるため)
    probe_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe_socket.bind(("127.0.0.1", 0))
    port = probe_socket.getsockname()[1]
    probe_socket.close()

    # start_echo_serverはブロッキングするので、別スレッド(デーモン化)で起動する
    server_thread = threading.Thread(
        target=start_echo_server, args=("127.0.0.1", port), daemon=True
    )
    server_thread.start()
    time.sleep(0.2)  # サーバーがaccept待ちになるまで少し待つ

    message = "サーバー疎通確認テストです"
    print(f"  127.0.0.1:{port} のエコーサーバーに接続し、'{message}' を送信します")
    response = send_echo_message("127.0.0.1", port, message)
    print(f"  受け取った応答: '{response}'")
    print(f"  送信内容と一致するか: {response == message}")


def main():
    print("=" * 60)
    print("1. socketモジュールの基礎(TCP接続によるポート疎通確認)")
    print("=" * 60)
    demo_port_check()

    print()
    print("=" * 60)
    print("2-a. requestsライブラリでのHTTP通信(依存性注入)")
    print("=" * 60)
    demo_http_status_with_dependency_injection()

    print()
    print("=" * 60)
    print("2-b. unittest.mockでrequests.getそのものをモックする")
    print("=" * 60)
    demo_http_status_with_mock()

    print()
    print("=" * 60)
    print("3. json.loads / json.dumps によるデータのやり取り")
    print("=" * 60)
    demo_json_parsing()

    print()
    print("=" * 60)
    print("4. socketモジュールで作る簡易エコーサーバー")
    print("=" * 60)
    demo_echo_server()


if __name__ == "__main__":
    main()

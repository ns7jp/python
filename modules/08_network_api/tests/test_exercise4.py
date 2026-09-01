"""演習4のテスト: start_echo_server / send_echo_message

127.0.0.1上でstart_echo_serverをバックグラウンドスレッド(daemon=True)で
起動し、send_echo_messageで実際に送受信できることを確認する。
ポート番号は固定値を決め打ちにせず、socket.bind(("127.0.0.1", 0))で
一時的に空きポートを取得してから、そのポート番号を使ってサーバーを
起動することでポート競合を避けている。
"""
import socket
import threading
import time

from exercises.exercise4 import send_echo_message, start_echo_server


def _find_free_port():
    """127.0.0.1上で現在空いているポート番号を1つ取得する。

    一時的にソケットをbindしてポート番号を取得したあとすぐにcloseし、
    その番号をサーバー起動用に使う。ごく短い時間の隙間はあるが、
    ローカルのテスト環境で固定ポートを決め打ちするより安全である。
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _start_server_thread(host, port):
    thread = threading.Thread(
        target=start_echo_server, args=(host, port), daemon=True
    )
    thread.start()
    # サーバーがbind/listenを終えてaccept待ちになるまで少し待つ
    time.sleep(0.2)
    return thread


def test_send_echo_message_returns_same_message():
    host = "127.0.0.1"
    port = _find_free_port()
    _start_server_thread(host, port)

    result = send_echo_message(host, port, "こんにちは、サーバー!")
    assert result == "こんにちは、サーバー!"


def test_send_echo_message_with_ascii_text():
    host = "127.0.0.1"
    port = _find_free_port()
    _start_server_thread(host, port)

    result = send_echo_message(host, port, "ping")
    assert result == "ping"


def test_send_echo_message_returns_str_type():
    host = "127.0.0.1"
    port = _find_free_port()
    _start_server_thread(host, port)

    result = send_echo_message(host, port, "type-check")
    assert isinstance(result, str)

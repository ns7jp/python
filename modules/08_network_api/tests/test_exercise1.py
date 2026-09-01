"""演習1のテスト: is_port_open

外部ネットワークには一切アクセスせず、127.0.0.1(ローカルホスト)上に
自分でソケットサーバーを立てて疎通確認のテストを行う。
ポート番号は固定値を決め打ちせず、socket.bind(("127.0.0.1", 0))で
その都度空いているポートを動的に取得することで、他のテストや
別プロセスとのポート競合を避けている。
"""
import socket

from exercises.exercise1 import is_port_open


def _get_free_port_socket():
    """127.0.0.1上で空いているポートにbindしたソケットを返す。

    ポート番号は0を指定することでOSに自動的に選んでもらう。
    戻り値のソケットのgetsockname()[1]で、実際に割り当てられた
    ポート番号を確認できる。
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    return s


def test_is_port_open_returns_true_when_listening():
    server = _get_free_port_socket()
    port = server.getsockname()[1]
    server.listen(1)
    try:
        assert is_port_open("127.0.0.1", port) is True
    finally:
        server.close()


def test_is_port_open_returns_false_when_nothing_listening():
    # bindだけしてlistenせずにすぐcloseする -> ポートは解放され、
    # 接続を試みるとConnection Refusedになる(何も待ち受けていない)
    server = _get_free_port_socket()
    port = server.getsockname()[1]
    server.close()

    assert is_port_open("127.0.0.1", port) is False


def test_is_port_open_returns_bool_type():
    server = _get_free_port_socket()
    port = server.getsockname()[1]
    server.listen(1)
    try:
        result = is_port_open("127.0.0.1", port)
    finally:
        server.close()
    assert isinstance(result, bool)

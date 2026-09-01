"""演習4の模範解答: 簡易エコーサーバーを自分で実装する

仕様の詳細はexercises/exercise4.pyのdocstringを参照してください。
"""
import socket


def start_echo_server(host, port):
    """指定host:portでTCPソケットをbindし、1接続分だけエコー処理を行う。

    仕様はexercises/exercise4.pyのdocstringを参照。
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
    """指定host:portにTCP接続し、messageを送信して応答を文字列で受け取る。

    仕様はexercises/exercise4.pyのdocstringを参照。
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.sendall(message.encode("utf-8"))
        data = sock.recv(4096)
    return data.decode("utf-8")

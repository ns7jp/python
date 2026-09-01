"""演習1の模範解答: socketモジュールでTCPポートの疎通確認をする

仕様の詳細はexercises/exercise1.pyのdocstringを参照してください。
"""
import socket


def is_port_open(host, port, timeout=1.0):
    """指定したhost:portへTCP接続を試み、接続できるかどうかを調べる。

    仕様はexercises/exercise1.pyのdocstringを参照。
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        # ConnectionRefusedError, socket.timeout(TimeoutError) など、
        # 接続に関する例外はすべてOSErrorの派生クラスなのでまとめて捕まえる
        return False

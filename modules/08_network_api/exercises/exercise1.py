"""演習1: socketモジュールでTCPポートの疎通確認をする

サーバーエンジニアの仕事では、「あのサーバーの80番ポート(Webサーバー)は
開いているか?」「22番ポート(SSH)に接続できるか?」といった
「ポート疎通確認」を日常的に行います。この演習では、Python標準ライブラリの
`socket`モジュールを使って、指定したホスト・ポートにTCP接続できるかどうかを
確認する関数を作ります。

(注意) この演習では実在の外部サーバーには一切接続しません。テストコードの
中で自分でローカル(127.0.0.1)にソケットサーバーを立てて確認します。
"""
import socket


def is_port_open(host, port, timeout=1.0):
    """指定したhost:portへTCP接続を試み、接続できるかどうかを調べる。

    socketモジュールを使って、指定したホスト・ポートに対してTCP接続を
    試みます。接続に成功すればTrue、失敗すればFalseを返します。
    タイムアウトや接続拒否(サーバーが起動していない、ポートが
    閉じている、など)といった例外は、この関数の中でキャッチし、
    呼び出し元には例外を伝播させずにFalseに変換してください。

    引数:
        host (str): 接続先のホスト名またはIPアドレス(例: "127.0.0.1")。
        port (int): 接続先のポート番号(例: 22, 80, 8080)。
        timeout (float): 接続を試みる際のタイムアウト秒数。デフォルトは1.0秒。

    戻り値:
        bool: 接続に成功した場合はTrue、失敗(タイムアウト・接続拒否・
            その他の通信エラー)した場合はFalse。

    入出力例:
        >>> is_port_open("127.0.0.1", 22)  # SSHサーバーが起動していれば
        True
        >>> is_port_open("127.0.0.1", 65000)  # 何も待ち受けていないポート
        False

    ヒント:
        - `socket.create_connection((host, port), timeout=timeout)` を
          `with`文と組み合わせて使うと、接続の成功・失敗を簡潔に判定でき、
          接続後のクローズ忘れも防げます。
        - 接続に失敗すると`OSError`(の派生クラス。例:
          `ConnectionRefusedError`や`socket.timeout`)が発生します。
    """
    # TODO: socket.create_connection((host, port), timeout=timeout) を
    #       try節の中で呼び出し、成功したらTrueを返してください。
    #       OSError(ConnectionRefusedErrorやsocket.timeoutを含む)が
    #       発生した場合はexcept節でFalseを返してください。
    raise NotImplementedError("is_port_open を実装してください")

"""演習4(応用): 簡易エコーサーバーを自分で実装する

これまでの演習では「接続できるかどうか」「レスポンスを解析する」といった
クライアント側の視点を扱いました。この演習では逆に、TCPソケットで
「待ち受け(サーバー)」側を自分の手で実装します。仕組みそのものを
自分で書いてみることで、「HTTPサーバーやSSHサーバーが裏側で何を
しているのか」のイメージがぐっとつかみやすくなります。

作るのは「エコーサーバー」、つまり「送られてきたデータをそのまま
送り返すだけ」のとてもシンプルなサーバーです。
"""
import socket


def start_echo_server(host, port):
    """指定host:portでTCPソケットをbindし、1接続分だけエコー処理を行う。

    処理の流れ:
        1. socket.socket(...)でTCPソケットを作成する
        2. socket.bind((host, port))で指定のアドレスに割り当てる
        3. socket.listen(...)で接続待ち状態にする
        4. socket.accept()で1つの接続を受け付ける(この呼び出しは、
           クライアントが接続してくるまでブロッキングする)
        5. 受信したデータを、そのまま同じ接続に送り返す(エコーする)
        6. 接続・ソケットを閉じて関数を終える

    (重要) この関数は「1接続を受け付けて処理が終わったら関数も終了する」
    ブロッキングな作りです。accept()を呼んだ時点でクライアントが
    接続してくるまで処理が止まる(ブロックする)ため、この関数を
    呼び出す側は、メインの処理を止めないように、あらかじめ
    `threading.Thread(target=start_echo_server, args=(host, port), daemon=True).start()`
    のように**別スレッド**で起動することを想定しています
    (daemon=Trueにしておくと、メインプログラムが終了するときに
    このスレッドも一緒に終了してくれます)。

    引数:
        host (str): bindするホスト(例: "127.0.0.1")。
        port (int): bindするポート番号。0を指定するとOSが空いている
            ポートを自動的に割り当てる(この関数自身は割り当てられた
            実際のポート番号を返さない点に注意。テストなどで実際の
            ポート番号を知りたい場合は、別のソケットで先に空きポートを
            調べてから、その番号をこの関数に渡すとよい)。

    戻り値:
        None

    入出力例:
        >>> import threading
        >>> t = threading.Thread(
        ...     target=start_echo_server, args=("127.0.0.1", 50007), daemon=True
        ... )
        >>> t.start()
        >>> # この後、別のクライアントが127.0.0.1:50007に接続すると、
        >>> # 送ったデータがそのまま返ってくる
    """
    # TODO: 1. socket.socket(socket.AF_INET, socket.SOCK_STREAM)でソケットを作成
    #       2. socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)で
    #          ポートの再利用を許可しておく(推奨)
    #       3. server_socket.bind((host, port))でアドレスを割り当てる
    #       4. server_socket.listen(1)で接続待ちにする
    #       5. conn, addr = server_socket.accept()で1接続を受け付ける
    #       6. conn.recv(4096)でデータを受信する
    #       7. 受信したデータをconn.sendall(...)でそのまま送り返す
    #       8. finally節などでconnとserver_socketを必ずcloseする
    raise NotImplementedError("start_echo_server を実装してください")


def send_echo_message(host, port, message, timeout=2.0):
    """指定host:portにTCP接続し、messageを送信して応答を文字列で受け取る。

    処理の流れ:
        1. socket.socket(...)でTCPソケットを作成する
        2. socket.connect((host, port))で接続する
        3. messageを`.encode("utf-8")`でバイト列に変換して送信する
        4. サーバーからの応答をバイト列で受信する
        5. 受信したバイト列を`.decode("utf-8")`で文字列に変換して返す

    引数:
        host (str): 接続先ホスト(例: "127.0.0.1")。
        port (int): 接続先ポート番号。
        message (str): サーバーに送信する文字列。
        timeout (float): 接続・通信のタイムアウト秒数。デフォルトは2.0秒。

    戻り値:
        str: サーバーから返ってきた(エコーされた)文字列。

    入出力例:
        >>> # 127.0.0.1:50007 でstart_echo_serverが動作している前提
        >>> send_echo_message("127.0.0.1", 50007, "こんにちは")
        'こんにちは'
    """
    # TODO: 1. socket.socket(socket.AF_INET, socket.SOCK_STREAM)でソケットを作成
    #          (with文を使うと、送受信が終わったら自動的にcloseされて便利です)
    #       2. sock.settimeout(timeout)でタイムアウトを設定する
    #       3. sock.connect((host, port))で接続する
    #       4. sock.sendall(message.encode("utf-8"))で送信する
    #       5. data = sock.recv(4096)で応答を受信する
    #       6. return data.decode("utf-8")で文字列に変換して返す
    raise NotImplementedError("send_echo_message を実装してください")

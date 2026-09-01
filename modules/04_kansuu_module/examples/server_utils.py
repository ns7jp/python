"""examples/example.py から読み込まれる補助モジュール。

このように、関連する処理を別ファイル(モジュール)にまとめておくと、
呼び出し側のファイルはすっきりし、他の場所からも再利用しやすくなります。
これが「モジュール分割」の基本的な考え方です。
"""


def build_status_line(server_name, status):
    """サーバー名と状態から、ログ風の1行の文字列を作る。

    引数:
        server_name (str): サーバー名。
        status (str): サーバーの状態("active" など)。

    戻り値:
        str: アイコン付きの1行の文字列。
    """
    icon = "✅" if status == "active" else "⚠️"
    return f"{icon} {server_name}: {status}"

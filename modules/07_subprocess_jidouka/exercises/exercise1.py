"""演習1: subprocess.run で外部コマンドを実行し、結果を受け取る

サーバー運用の自動化スクリプトでは、Pythonの中から `df -h`(ディスク使用量の
確認)や `systemctl status nginx`(サービスの状態確認)のような外部コマンドを
実行し、その「結果」(成功したか失敗したか、何が出力されたか)をプログラムで
扱いたい場面がよくあります。この演習では、標準ライブラリの `subprocess`
モジュールを使って、外部コマンドを実行しその結果を取得する最も基本的な
関数を実装します。
"""
import subprocess


def run_command(command):
    """外部コマンドを実行し、(returncode, 標準出力の文字列) のタプルを返す。

    subprocess.run() を使って command を実行する。以下のオプションを
    必ず指定すること。

    - capture_output=True: 標準出力・標準エラー出力を受け取れるようにする
    - text=True: 出力をバイト列(bytes)ではなく文字列(str)として扱う

    引数:
        command (list[str]): 実行するコマンドと引数を並べたリスト。
            例: ["echo", "hello"] や ["python3", "-c", "print(1)"]
            シェルの文法(パイプやリダイレクトなど)は使えない、
            単純な「コマンド名 + 引数」のリストであることに注意。

    戻り値:
        tuple[int, str]: (returncode, stdout) のタプル。
            - returncode (int): コマンドの終了コード。0であれば正常終了。
            - stdout (str): コマンドの標準出力(文字列)。

    入出力例:
        >>> run_command(["echo", "hello"])
        (0, "hello\\n")
        >>> returncode, stdout = run_command(["python3", "-c", "print('hi')"])
        >>> returncode
        0
        >>> stdout
        "hi\\n"
    """
    # TODO: subprocess.run(command, capture_output=True, text=True) を実行し、
    #       結果オブジェクトの .returncode と .stdout をタプルにして返してください。
    raise NotImplementedError("run_command を実装してください")

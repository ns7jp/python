"""演習2: returncode を見て「成功したかどうか」を判定する

サーバー監視スクリプトの多くは、「コマンドの出力内容」そのものよりも
「そのコマンドが成功したか失敗したか」だけを知りたい場面が多くあります。
Linuxのコマンドは慣習として、正常終了したときは returncode(終了コード)に
0 を、何らかの問題があったときは 0 以外の値を返します。この演習では、
その慣習を利用して「成功/失敗」を bool 値で判定する関数を実装します。
"""
import subprocess


def is_command_successful(command):
    """外部コマンドを実行し、正常終了(returncode == 0)したかどうかを返す。

    演習1の run_command と同じ考え方で command を subprocess.run() で
    実行し、capture_output=True と text=True を指定する。実行結果の
    returncode が 0 であれば True、0 以外であれば False を返す。

    引数:
        command (list[str]): 実行するコマンドと引数を並べたリスト。
            例: ["echo", "ok"] や ["python3", "-c", "exit(1)"]

    戻り値:
        bool: returncode が 0 なら True、それ以外なら False。

    入出力例:
        >>> is_command_successful(["echo", "ok"])
        True
        >>> is_command_successful(["python3", "-c", "exit(1)"])
        False
        >>> is_command_successful(["python3", "-c", "exit(0)"])
        True
    """
    # TODO: subprocess.run(command, capture_output=True, text=True) を実行し、
    #       結果の .returncode が 0 かどうかを bool で返してください。
    raise NotImplementedError("is_command_successful を実装してください")

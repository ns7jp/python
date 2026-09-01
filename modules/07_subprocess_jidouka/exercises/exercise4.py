"""演習4(応用): 複数サービスのヘルスチェックレポートを作る

サーバー運用の現場では、「webサーバーは動いているか」「DBサーバーは
動いているか」など、複数のサービスの状態をまとめて確認し、レポートとして
まとめる作業がよくあります。cronで定期実行するヘルスチェックスクリプトの
典型的な形です。この演習では、演習1・演習2で学んだ「コマンドを実行して
returncodeを見る」という考え方を、複数サービス分まとめて行う関数を
実装します。
"""
import subprocess


def build_health_check_script_report(commands):
    """複数サービスのコマンドを実行し、サービスごとの成功/失敗をまとめる。

    commands は「サービス名の文字列」をキー、「実行するコマンド
    (文字列のリスト)」を値とする辞書。この関数は各サービスについて
    コマンドを実行し(演習1のrun_commandや演習2のis_command_successfulと
    同じ考え方で subprocess.run を使う)、returncodeが0であれば成功
    (True)、それ以外であれば失敗(False)として、
    {サービス名: 成功したかどうか(bool)} の辞書にまとめて返す。

    引数:
        commands (dict[str, list[str]]): サービス名をキー、実行する
            コマンド(文字列のリスト)を値とする辞書。
            例: {"web": ["echo", "ok"], "db": ["python3", "-c", "exit(1)"]}

    戻り値:
        dict[str, bool]: サービス名をキー、そのコマンドが正常終了
            (returncode == 0)したかどうかを値とする辞書。

    入出力例:
        >>> build_health_check_script_report({
        ...     "web": ["echo", "ok"],
        ...     "db": ["python3", "-c", "exit(1)"],
        ... })
        {"web": True, "db": False}
    """
    # TODO: commandsの各(サービス名, コマンド)の組についてsubprocess.runを実行し、
    #       returncode == 0 かどうかを結果の辞書に詰めて返してください。
    #       (辞書内包表記を使うと簡潔に書けますが、forループでも構いません)
    raise NotImplementedError("build_health_check_script_report を実装してください")

"""演習2の模範解答: 独自例外クラスを定義して、意味の伝わるエラーを表現する

仕様の詳細はexercises/exercise2.pyのdocstringを参照してください。
"""


class ServerUnreachableError(Exception):
    """サーバーに到達できない(疎通確認に失敗した)ことを表す独自例外。

    仕様はexercises/exercise2.pyのdocstringを参照。
    """

    pass


def check_server(is_reachable, name):
    """サーバーの疎通確認を行う(結果に応じて例外をraiseする)。

    仕様はexercises/exercise2.pyのdocstringを参照。
    """
    if not is_reachable:
        raise ServerUnreachableError(f"サーバー{name}に到達できません")
    return f"サーバー{name}: 到達可能"


def check_server_safe(is_reachable, name):
    """check_serverを呼び出し、例外が起きても安全にメッセージを返す。

    仕様はexercises/exercise2.pyのdocstringを参照。
    """
    try:
        return check_server(is_reachable, name)
    except ServerUnreachableError:
        return f"エラー: サーバー{name}: 到達できません"

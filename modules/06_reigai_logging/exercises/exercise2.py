"""演習2: 独自例外クラスを定義して、意味の伝わるエラーを表現する

Python標準の例外(ValueErrorやZeroDivisionErrorなど)だけでなく、
「このプログラム独自の異常事態」を表す例外クラスを自分で定義することも
できます。サーバー監視ツールであれば「サーバーに到達できない」という
状況は頻繁に発生するので、それ専用の例外クラスを用意しておくと、
エラーの種類がひと目で分かるようになり、後から対応するコードも
書きやすくなります。
"""


class ServerUnreachableError(Exception):
    """サーバーに到達できない(疎通確認に失敗した)ことを表す独自例外。

    サーバー監視やヘルスチェックの処理で、対象サーバーへの接続・応答が
    確認できなかった場合にraiseする。Exceptionクラスを継承しているだけの
    シンプルな例外クラスだが、「ValueErrorやTypeErrorのような汎用的な
    例外ではなく、サーバー到達不可という具体的な異常事態である」ことを
    コード上で明示できる点が重要。呼び出し側は
    `except ServerUnreachableError:` のように、この種類の異常だけを
    ピンポイントで捕まえられる。
    """

    pass


def check_server(is_reachable, name):
    """サーバーの疎通確認を行う(結果に応じて例外をraiseする)。

    is_reachable が False の場合は、サーバーに到達できなかったとみなし、
    ServerUnreachableError をraiseする。True の場合は到達できたことを
    表す文字列を返す。

    (注意) 実際の監視ツールでは is_reachable の部分がping確認や
    HTTPリクエストの結果になりますが、本演習では外部ネットワークに
    依存しないよう、疎通結果をあらかじめbool値として引数で受け取る
    設計にしています。

    引数:
        is_reachable (bool): サーバーに到達できたかどうか。
        name (str): サーバー名。

    戻り値:
        str: is_reachable が True の場合、"サーバー{name}: 到達可能"
            という文字列。

    例外:
        ServerUnreachableError: is_reachable が False の場合に発生する。

    入出力例:
        >>> check_server(True, "web01")
        'サーバーweb01: 到達可能'
        >>> check_server(False, "web01")
        (ServerUnreachableErrorが発生する)
    """
    # TODO: is_reachable が False の場合、
    #       ServerUnreachableError(f"サーバー{name}に到達できません") を
    #       raiseしてください。
    #       True の場合は f"サーバー{name}: 到達可能" を返してください。
    raise NotImplementedError("check_server を実装してください")


def check_server_safe(is_reachable, name):
    """check_serverを呼び出し、例外が起きても安全にメッセージを返す。

    内部で check_server(is_reachable, name) を呼び出す。
    ServerUnreachableError が発生した場合は、try/exceptでそれを捕まえ、
    例外を外に投げる代わりにエラーメッセージの文字列を返す。
    このように「例外を捕まえて、呼び出し元が扱いやすい戻り値に変換する」
    処理は、監視スクリプトなどでプログラムを止めずに次のサーバーの
    チェックを続けたい場合によく使われる。

    引数:
        is_reachable (bool): サーバーに到達できたかどうか。
        name (str): サーバー名。

    戻り値:
        str: 到達できた場合は check_server と同じ
            "サーバー{name}: 到達可能"。
            到達できなかった場合は "エラー: サーバー{name}: 到達できません"。

    入出力例:
        >>> check_server_safe(True, "web01")
        'サーバーweb01: 到達可能'
        >>> check_server_safe(False, "web01")
        'エラー: サーバーweb01: 到達できません'
    """
    # TODO: try節でcheck_server(is_reachable, name)を呼び出して返してください。
    #       except ServerUnreachableError: の節で
    #       f"エラー: サーバー{name}: 到達できません" を返してください。
    raise NotImplementedError("check_server_safe を実装してください")

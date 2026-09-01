"""
演習3: ポート番号文字列のパース(例外を投げる関数)

この章の exercises/ には、すでに完成した「テスト対象のコード」が
入っています。学習者が編集するのは tests/ 側です。
"""


def parse_port(value):
    """
    文字列valueを受け取り、ポート番号を表すintに変換して返す。

    サーバーの設定ファイルや環境変数からポート番号を読み込むとき、
    値は文字列として渡されることがほとんどです。この関数では、その
    文字列が正しいポート番号(0〜65535)を表しているかどうかを確認
    しながら、intに変換します。

    引数:
        value (str): ポート番号を表す文字列。

    戻り値:
        int: 変換後のポート番号。

    例外:
        ValueError: 以下のいずれかの場合に送出する。
            - valueが整数として解釈できない文字列の場合
              (例: "abc", "80.5", "" など)
            - 変換後の値が0〜65535の範囲外の場合
              (例: "-1", "70000")

    入出力例:
        >>> parse_port("8080")
        8080
        >>> parse_port("0")
        0
        >>> parse_port("70000")
        Traceback (most recent call last):
            ...
        ValueError: ポート番号は0〜65535の範囲で指定してください: 70000
        >>> parse_port("abc")
        Traceback (most recent call last):
            ...
        ValueError: 数値として解釈できません: abc
    """
    try:
        port = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"数値として解釈できません: {value}")

    if port < 0 or port > 65535:
        raise ValueError(f"ポート番号は0〜65535の範囲で指定してください: {port}")

    return port

"""
演習2: 簡易的なホスト名バリデーション

この章の exercises/ には、すでに完成した「テスト対象のコード」が
入っています。学習者が編集するのは tests/ 側です。
"""


def is_valid_hostname(hostname):
    """
    文字列hostnameが、簡易的なホスト名として妥当かどうかを判定する。

    サーバー構築の現場では、設定ファイルに書くホスト名の形式が正しいかを
    事前にチェックすることで、タイプミスなどによる設定ミスを未然に防ぐ
    ことができます。ここでは以下の条件をすべて満たす場合にTrueを返す、
    簡易的なバリデーション(検証)を実装しています。
    (実際のRFC仕様に完全準拠したホスト名チェックではありません)

    条件:
        1. 空文字列でないこと
        2. 全体の長さが253文字以下であること
        3. 英数字(a-z, A-Z, 0-9)・ハイフン(-)・ドット(.)のみで
           構成されていること
        4. 先頭と末尾がハイフン(-)でないこと

    引数:
        hostname (str): 検証したいホスト名の文字列。

    戻り値:
        bool: 条件をすべて満たせばTrue、そうでなければFalse。

    入出力例:
        >>> is_valid_hostname("web01.example.com")
        True
        >>> is_valid_hostname("")
        False
        >>> is_valid_hostname("-web01")
        False
        >>> is_valid_hostname("web_01")
        False
    """
    if not hostname:
        return False
    if len(hostname) > 253:
        return False

    allowed_chars = set(
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "-."
    )
    if not set(hostname).issubset(allowed_chars):
        return False

    if hostname.startswith("-") or hostname.endswith("-"):
        return False

    return True

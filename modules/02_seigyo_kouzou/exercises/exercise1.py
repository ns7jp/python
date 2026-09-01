"""演習1: ポート番号を分類する

サーバーエンジニアの仕事では、TCP/UDPの「ポート番号」がどの種類に
属するかを判断する場面がよくあります。この演習では if/elif/else を使って
ポート番号を4つのカテゴリに分類する関数を実装します。
"""


def check_port_status(port):
    """ポート番号を受け取り、その種類を表す文字列を返す。

    ポート番号の区分(IANAの分類に基づく一般的な目安):
        0〜1023      : "システムポート"     (well-known port とも呼ばれる)
        1024〜49151  : "登録済みポート"     (registered port)
        49152〜65535 : "動的ポート"         (dynamic / private port)
        上記以外     : "無効なポート"       (ポート番号として不正な値)

    if/elif/else を使って実装すること。

    引数:
        port (int): 判定したいポート番号。

    戻り値:
        str: ポートの区分を表す文字列。

    入出力例:
        >>> check_port_status(22)
        'システムポート'
        >>> check_port_status(8080)
        '登録済みポート'
        >>> check_port_status(50000)
        '動的ポート'
        >>> check_port_status(-1)
        '無効なポート'
        >>> check_port_status(70000)
        '無効なポート'
    """
    # TODO: if/elif/else を使ってポート番号を分類し、対応する文字列を返してください。
    raise NotImplementedError("check_port_status を実装してください")

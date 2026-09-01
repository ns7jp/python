"""演習3: pingコマンドの出力テキストを解析する

サーバー監視スクリプトでは「あるホストに到達できるか」を調べるために
`ping` コマンドがよく使われます。ただし、この演習パックは外部ネットワーク
への実アクセスを行わない方針のため、実際に ping コマンドを実行するのでは
なく、「pingコマンドが出力しそうなテキスト」をあらかじめ用意した文字列と
して受け取り、それを解析する関数を実装します。実務でも、コマンドの出力を
文字列として受け取ってから解析する、という流れ自体は同じです
(演習1・2で学んだ run_command が返す stdout を、この関数に渡すイメージです)。

Linuxの ping コマンドは、実行結果の末尾付近に
"3 packets transmitted, 3 received, 0% packet loss, time 2004ms"
のような統計行を出力します。この "0% packet loss" という部分に注目すると、
パケットロス(送ったデータが届かなかった割合)が0%かどうか、つまり
「完全に到達できたかどうか」を判定できます。
"""


def parse_ping_output(ping_output):
    """pingコマンドの標準出力を模したテキストを解析し、到達可能かを返す。

    実際に ping コマンドを実行することはしない。あらかじめ用意された
    ping_output(pingコマンドが出力しそうな文字列)の中に
    "0% packet loss" という文字列が含まれているかどうかだけを調べる。

    引数:
        ping_output (str): pingコマンドの標準出力を模したテキスト。
            例:
            "PING example.com (93.184.216.34): 56 data bytes\\n"
            "64 bytes from 93.184.216.34: icmp_seq=0 ttl=56 time=12.3 ms\\n"
            "--- example.com ping statistics ---\\n"
            "3 packets transmitted, 3 received, 0% packet loss, time 2004ms\\n"

    戻り値:
        bool: ping_output に "0% packet loss" が含まれていれば True
            (到達可能)、含まれていなければ False(到達不可・一部ロス)。

    入出力例:
        >>> parse_ping_output(
        ...     "3 packets transmitted, 3 received, 0% packet loss, time 2004ms"
        ... )
        True
        >>> parse_ping_output(
        ...     "3 packets transmitted, 1 received, 67% packet loss, time 2010ms"
        ... )
        False

    (発展メモ) この関数は単純な部分文字列の検索です。そのため、
    たとえば "100% packet loss" のように、たまたま末尾が "0%" に
    なっている文字列も、部分文字列としては "0% packet loss" を
    含んでしまうため True と判定されてしまいます。この単純な実装の
    限界に興味がある人は、README の「7. 発展課題」も見てみましょう。
    """
    # TODO: "0% packet loss" という文字列が ping_output に含まれているかを
    #       in 演算子で判定し、bool値として返してください。
    raise NotImplementedError("parse_ping_output を実装してください")

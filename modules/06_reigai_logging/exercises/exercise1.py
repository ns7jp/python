"""演習1: 例外を「握りつぶさず」安全に処理する

サーバー運用スクリプトでは、想定外の値が渡されてきてもプログラム全体を
異常終了させたくない場面がよくあります。この演習では try/except を使い、
特定の例外が発生したときだけNoneを返す「安全な」関数を実装します。

(注意) 何でもかんでも例外を握りつぶすのは良い設計ではありませんが、
「起こりうることが分かっている例外」を、呼び出し元に伝わりやすい形
(ここでは戻り値がNoneかどうか)に変換するのは、実務でもよく使われる
テクニックです。
"""


def safe_divide(a, b):
    """aをbで割った結果を返す。ゼロ除算が起きてもプログラムを止めない。

    b が 0 の場合、a / b は ZeroDivisionError という例外を発生させる。
    この関数では try/except を使ってその例外を捕まえ、例外を外に
    伝播させる(呼び出し元にまでエラーを届けてしまう)代わりに、
    Noneを返すようにする。

    引数:
        a (int | float): 割られる数。
        b (int | float): 割る数。

    戻り値:
        int | float | None: a / b の結果。ただし b が 0 で
            ZeroDivisionError が発生した場合は None。

    入出力例:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0)
        (Noneが返る。例外は発生しない)
        >>> safe_divide(-9, 3)
        -3.0
    """
    # TODO: try節で a / b を計算して返してください。
    #       except ZeroDivisionError: の節で None を返してください。
    raise NotImplementedError("safe_divide を実装してください")


def parse_int_safe(value):
    """文字列valueをintに変換する。変換できない場合はNoneを返す。

    int(value) は、value が整数として解釈できない文字列
    (例: "abc" や "12.5" や "") の場合に ValueError という例外を
    発生させる。この関数では try/except を使ってその例外を捕まえ、
    Noneを返すようにする。

    引数:
        value (str): 整数に変換したい文字列。

    戻り値:
        int | None: 変換に成功した場合はint型の値。
            ValueErrorが発生した場合はNone。

    入出力例:
        >>> parse_int_safe("42")
        42
        >>> parse_int_safe("abc")
        (Noneが返る。例外は発生しない)
        >>> parse_int_safe("-7")
        -7
    """
    # TODO: try節で int(value) を計算して返してください。
    #       except ValueError: の節で None を返してください。
    raise NotImplementedError("parse_int_safe を実装してください")

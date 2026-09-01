"""演習1の模範解答: 例外を「握りつぶさず」安全に処理する

仕様の詳細はexercises/exercise1.pyのdocstringを参照してください。
"""


def safe_divide(a, b):
    """aをbで割った結果を返す。ゼロ除算が起きてもプログラムを止めない。

    仕様はexercises/exercise1.pyのdocstringを参照。
    """
    try:
        return a / b
    except ZeroDivisionError:
        return None


def parse_int_safe(value):
    """文字列valueをintに変換する。変換できない場合はNoneを返す。

    仕様はexercises/exercise1.pyのdocstringを参照。
    """
    try:
        return int(value)
    except ValueError:
        return None

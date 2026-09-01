"""
演習3: ポート番号の妥当性チェック (難易度: ★★☆)

型チェック(isinstance)・比較演算子・論理演算子を練習します。
"""


def is_valid_port(port):
    """引数がポート番号として妥当かどうかを判定する。

    「妥当なポート番号」とは、0以上65535以下の「整数」であることとする。
    次のような入力は、いずれもFalseと判定すること(型チェックが必要):

    - 文字列(例: "8080"): 数字に見えても str 型なので False
    - 小数(例: 8080.0): float 型なので、値が整数と等しく見えても False
    - 範囲外の整数(例: -1, 70000): 整数だが範囲外なので False
    - bool値(True / False): Pythonでは bool は int のサブクラスであり
      isinstance(True, int) は True になってしまうが、
      「ポート番号」としては意味を持たないため、
      True/False が渡された場合は必ず False を返すこと

    引数:
        port: ポート番号として妥当かどうかを調べたい値(型は問わない)

    戻り値:
        bool: 0以上65535以下の整数であればTrue、それ以外はFalse

    入出力例:
        >>> is_valid_port(8080)
        True
        >>> is_valid_port(0)
        True
        >>> is_valid_port(65535)
        True
        >>> is_valid_port(70000)
        False
        >>> is_valid_port(-1)
        False
        >>> is_valid_port("8080")
        False
        >>> is_valid_port(8080.0)
        False
        >>> is_valid_port(True)
        False
    """
    # TODO: まず port が bool 型かどうかをチェックし、bool なら False を返す
    # TODO: 次に port が int 型かどうかを isinstance() でチェックし、int でなければ False を返す
    # TODO: 最後に 0 <= port <= 65535 の範囲かどうかを判定して返す
    raise NotImplementedError("is_valid_port を実装してください")

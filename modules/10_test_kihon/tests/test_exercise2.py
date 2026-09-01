"""
演習2のテスト雛形: is_valid_hostname関数をテストしよう 📝

有効なホスト名の例と、無効なホスト名の例、それぞれについて
assert文を書いてテストしてみましょう。

1つのテスト関数の中に、複数のassert文を書いてもかまいません。
どれか1つでもFalseになれば、そのテスト関数全体が失敗(fail)になります。
"""

from exercises.exercise2 import is_valid_hostname


def test_is_valid_hostname_valid_cases():
    """
    有効なホスト名の例をテストする。

    例:
        - "web01.example.com" (英数字・ドット・ハイフンのみ)
        - "db-01"              (ハイフンを含むが先頭末尾ではない)
        - "192.168.0.1"        (数字とドットのみ)
    """
    # TODO: 上記のような有効なホスト名を複数パターン用意し、
    #       is_valid_hostname(...) の戻り値が True になることを
    #       assert文で確認しよう
    # ヒント: assert is_valid_hostname("web01.example.com") is True
    pass


def test_is_valid_hostname_invalid_cases():
    """
    無効なホスト名の例をテストする。

    例:
        - 空文字列 ""
        - 記号(アンダースコアなど)を含む文字列 "web_01"
        - 先頭がハイフンの文字列 "-web01"
        - 末尾がハイフンの文字列 "web01-"
    """
    # TODO: 上記のような無効なホスト名を複数パターン用意し、
    #       is_valid_hostname(...) の戻り値が False になることを
    #       assert文で確認しよう
    pass

"""
演習1のテスト雛形: bytes_to_gb関数をテストしよう 📝

exercises/exercise1.py の bytes_to_gb 関数は、すでに完成しています。
このファイルでは、その関数が「本当に仕様通りに動くか」を確認するための
テストコードを、自分の手で書いてみましょう。

やること:
    1. 下の TODO コメントの位置に、assert文を書く
    2. ターミナルで次のコマンドを実行し、テストが通ることを確認する
           pytest modules/10_test_kihon/tests -v
    3. わからなくなったら solutions/test_exercise1.py を見てみましょう

assert文の基本形:
    assert 実際の値 == 期待する値
"""

from exercises.exercise1 import bytes_to_gb


def test_bytes_to_gb_normal_case():
    """
    通常のケースをテストする。

    例: 1073741824バイト(= 1024 * 1024 * 1024)は、ちょうど1.0GBになるはず。
    """
    # TODO: bytes_to_gb(1073741824) の戻り値が 1.0 になることを
    #       assert文で確認しよう
    # ヒント: assert bytes_to_gb(1073741824) == 1.0
    pass


def test_bytes_to_gb_zero_bytes():
    """
    0バイトのケースをテストする。

    0バイトは0.0GBになるはず。
    """
    # TODO: bytes_to_gb(0) の戻り値が 0.0 になることを assert文で確認しよう
    pass

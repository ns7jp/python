"""
examples/example.py
テストの基礎(pytest入門) - サンプルコード

このファイルは「python3 modules/10_test_kihon/examples/example.py」として
そのまま実行できるサンプルです。pytestを使わずに、Python標準の assert文
だけで「テストとはどういうものか」の雰囲気をつかんでもらうことが目的です。

実際の開発では、ここで手作業でやっていることを pytest というツールに
任せます。pytestを使うと、
    - assert文が失敗したときに、期待値と実際の値をわかりやすく表示してくれる
    - テスト関数を自動的に集めて、まとめて実行してくれる
    - pytest.raises のような便利な仕組みで、例外の発生も簡単にテストできる
    - フィクスチャ(fixture)で、テストの前準備を使い回せる
といった恩恵を受けられます。この章の tests/ ディレクトリで、実際に
pytestを使ったテストコードを書く練習をします。

実行方法:
    cd /home/user/python
    python3 modules/10_test_kihon/examples/example.py
"""

import os
import sys

# このファイル(example.py)から見て1つ上の階層(この章のトップ
# ディレクトリ)をsys.pathに追加する。こうすることで、実行時の
# カレントディレクトリに関わらず「exercises」パッケージをimportできる。
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exercises.exercise1 import bytes_to_gb
from exercises.exercise2 import is_valid_hostname
from exercises.exercise3 import parse_port
from exercises.exercise4 import ServerRegistry


def section(title):
    """見出しを見やすく表示するだけの小さなヘルパー関数。"""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def demo_assert_basics():
    """
    1. assert文の基本

    assert文は「その条件がTrueであるはず」ということをコードの中で
    宣言する文です。条件がTrueなら何も起こらず次の行に進みますが、
    条件がFalseだと AssertionError という例外が発生してプログラムが
    止まります。

    サーバー運用スクリプトの中でも、「本来ありえないはずの状態」を
    早期に検知するために assert を使うことがあります。
    """
    section("1. assert文の基本")

    value = 1 + 1
    print(f"1 + 1 の計算結果: {value}")

    # 条件がTrueなら何も起こらない(正常に次の行へ進む)
    assert value == 2
    print("assert value == 2 は成功しました(何もエラーが出ません)")

    # あえて失敗するassertをtry/exceptで受け止めて、
    # どんなエラーになるかを確認してみます。
    try:
        assert value == 3, "1 + 1 は3にはならないはずです"
    except AssertionError as e:
        print(f"わざと失敗させたassertを捕まえました -> AssertionError: {e}")


def demo_function_under_test():
    """
    2. テスト対象の関数を、assertで手動テストしてみる

    exercises/exercise1.py の bytes_to_gb 関数を例に、
    「関数の戻り値が期待通りかどうか」をassert文で確認してみます。
    これはまさに、pytestのテスト関数の中でやっていることと同じです。
    """
    section("2. bytes_to_gb関数を手動でテストしてみる")

    result = bytes_to_gb(1073741824)
    print(f"bytes_to_gb(1073741824) の戻り値: {result}")
    assert result == 1.0
    print("期待通り 1.0 が返ってきました(assert成功)")

    result_zero = bytes_to_gb(0)
    print(f"bytes_to_gb(0) の戻り値: {result_zero}")
    assert result_zero == 0.0
    print("期待通り 0.0 が返ってきました(assert成功)")

    # pytestを使うと、これと同じ内容を
    #   def test_bytes_to_gb_normal_case():
    #       assert bytes_to_gb(1073741824) == 1.0
    # という「テスト関数」として書けます。
    # pytest コマンドを実行すると、test_ で始まる関数を自動的に見つけて
    # 実行し、結果(合格/不合格)をまとめて報告してくれます。
    print("\n(参考) pytestで同じ内容をテストするときのイメージ:")
    print('    def test_bytes_to_gb_normal_case():')
    print('        assert bytes_to_gb(1073741824) == 1.0')


def demo_hostname_validation():
    """
    3. is_valid_hostname関数を、複数パターンでテストしてみる

    1つの関数に対して、有効なパターン・無効なパターンの両方を
    テストすることが大切です。「正しい入力に対して正しく動く」だけ
    でなく、「不正な入力を正しく拒否できる」ことも確認しましょう。
    """
    section("3. is_valid_hostname関数を複数パターンでテストしてみる")

    valid_examples = ["web01.example.com", "db-01", "192.168.0.1"]
    invalid_examples = ["", "web_01", "-web01", "web01-"]

    for name in valid_examples:
        result = is_valid_hostname(name)
        print(f'is_valid_hostname("{name}") -> {result}')
        assert result is True

    for name in invalid_examples:
        result = is_valid_hostname(name)
        print(f'is_valid_hostname("{name}") -> {result}')
        assert result is False

    print("すべてのパターンで期待通りの結果になりました")


def demo_exception_testing():
    """
    4. 例外が発生することを確認するテスト(pytest.raisesの考え方)

    parse_port関数は、不正な値を渡すとValueErrorという例外を送出します。
    「例外が発生すること自体」が正しい動作なので、それをテストする
    必要があります。

    pytestには pytest.raises という専用の仕組みがあり、

        with pytest.raises(ValueError):
            parse_port("abc")

    のように書くだけで、「このブロックの中でValueErrorが発生すること」
    をテストできます。ここでは、pytestを使わずに同じことを
    try/exceptで手動で確認してみます。
    """
    section("4. 例外のテスト(pytest.raisesの考え方)")

    # 正常系: 例外が起きないケース
    port = parse_port("8080")
    print(f'parse_port("8080") -> {port} (正常に変換できました)')

    # 異常系: 例外が起きてほしいケース
    try:
        parse_port("abc")
        # ここに到達してしまったら、例外が発生しなかった = テスト失敗
        raise AssertionError("ValueErrorが発生しませんでした(想定外)")
    except ValueError as e:
        print(f'parse_port("abc") は期待通りValueErrorになりました: {e}')

    try:
        parse_port("70000")
        raise AssertionError("ValueErrorが発生しませんでした(想定外)")
    except ValueError as e:
        print(f'parse_port("70000") は期待通りValueErrorになりました: {e}')

    print("\n(参考) pytestで同じ内容をテストするときのイメージ:")
    print("    import pytest")
    print("    def test_parse_port_invalid():")
    print('        with pytest.raises(ValueError):')
    print('            parse_port("abc")')


def demo_fixture_style_setup():
    """
    5. fixtureの考え方(準備済みデータの使い回し)

    複数のテストで「同じ準備済みデータ」を使いたいことがよくあります。
    ここでは、ServerRegistryに2件のサーバーを登録した状態を作り、
    それを複数の「テストらしき処理」で使い回してみます。

    pytestでは、このような「準備」を @pytest.fixture を付けた関数として
    切り出すことができます。テスト関数の引数にfixture関数と同じ名前を
    書くだけで、pytestが自動的にその関数を呼び出し、戻り値を渡して
    くれます。詳しくはこの章のtests/test_exercise4.pyとREADME.mdで
    説明しています。
    """
    section("5. fixtureの考え方(準備済みデータの使い回し)")

    def build_registry():
        """
        pytestの @pytest.fixture 関数に相当する、準備用の関数。
        (ここではただのPython関数として書いていますが、
         pytestのfixtureも考え方はこれと同じです)
        """
        reg = ServerRegistry()
        reg.add_server("web01", {"ip": "192.168.0.1", "role": "web"})
        reg.add_server("db01", {"ip": "192.168.0.2", "role": "db"})
        return reg

    # 「テストその1」: get_serverの確認(毎回、新しいregistryを使う)
    registry = build_registry()
    print("registry.get_server('web01') ->", registry.get_server("web01"))
    assert registry.get_server("web01") == {"ip": "192.168.0.1", "role": "web"}

    # 「テストその2」: 未登録のサーバー名の確認
    registry = build_registry()
    print("registry.get_server('unknown') ->", registry.get_server("unknown"))
    assert registry.get_server("unknown") is None

    # 「テストその3」: list_namesの確認
    registry = build_registry()
    names = registry.list_names()
    print("registry.list_names() ->", names)
    assert set(names) == {"web01", "db01"}

    print("\nfixtureを使うと、この build_registry() のような準備処理を")
    print("何度も書かずに済み、テストコードがすっきりします。")


def demo_why_testing_matters():
    """
    6. なぜテストが必要か(サーバー運用の視点から)

    サーバー運用では、設定変更やスクリプトの修正のたびに、
    毎回手作業で「ちゃんと動くか」を確認するのは大変ですし、
    確認漏れがあると障害の原因になります。

    自動テストを書いておけば、
        - コードを変更したときに、すぐに壊れていないか確認できる
        - 何を確認すればよいかが、テストコード自体に記録される
        - GitHub ActionsなどのCI(継続的インテグレーション)で
          コードをpushするたびに自動でテストを実行できる
    といったメリットがあります。CIについては、この章のREADME.mdで
    もう少し詳しく説明しています。
    """
    section("6. なぜテストが必要か")
    print("- 手作業の確認だけに頼ると、確認漏れや思い込みでミスが起きやすい")
    print("- 自動テストがあれば、変更のたびに同じ確認を機械的に繰り返せる")
    print("- テストコードは『このコードが満たすべき仕様』の記録にもなる")
    print("- CI(GitHub Actionsなど)と組み合わせれば、pushするたびに")
    print("  自動でテストが走り、事故の少ない開発・運用につながる")


def main():
    """このサンプルスクリプトのエントリーポイント。上から順に各デモを実行する。"""
    print("Python基礎演習案件パック 第10章: テストの基礎(pytest入門)")
    print("サンプルコード example.py を実行します。")

    demo_assert_basics()
    demo_function_under_test()
    demo_hostname_validation()
    demo_exception_testing()
    demo_fixture_style_setup()
    demo_why_testing_matters()

    section("完了")
    print("すべてのデモが正常に完了しました。")
    print("次は tests/ ディレクトリのTODOを埋めて、pytestで実行してみましょう。")
    print("実行コマンド例: pytest modules/10_test_kihon/tests -v")


if __name__ == "__main__":
    main()

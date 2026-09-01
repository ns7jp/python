"""
第2章: 制御構造(if/elif/else, for, while, break, continue) サンプルコード
==========================================================================

このファイルは、サーバー運用でよく使う「条件分岐」と「繰り返し処理」を
実際に動かしながら確認するためのサンプルです。

実行方法:
    cd /home/user/python
    python3 modules/02_seigyo_kouzou/examples/example.py

外部ネットワークへのアクセスは一切行いません。すべてこのファイルの中だけで
完結するダミーデータ(疑似的なデータ)を使ってシミュレーションします。
"""


def classify_port(port):
    """ポート番号を if/elif/else で分類して文字列を返す小さなヘルパー関数。

    (演習1でみなさんが実装するのと似た内容です。仕組み理解のための例です)
    """
    if port < 0 or port > 65535:
        return "無効なポート"
    elif port <= 1023:
        return "システムポート"
    elif port <= 49151:
        return "登録済みポート"
    else:
        return "動的ポート"


def section1_if_elif_else():
    """1. if/elif/else によるポート番号の分類デモ。"""
    print("=" * 60)
    print("[1] if / elif / else : ポート番号の分類")
    print("=" * 60)

    # サーバーでよく使われる代表的なポート番号のリスト
    well_known_ports = [22, 80, 443, 3306, 8080, 50000, 70000]

    # for文でリストの要素を1つずつ取り出し、if/elif/elseで判定する
    for port in well_known_ports:
        category = classify_port(port)
        print(f"  ポート {port:>6} -> {category}")

    print()


def section2_for_and_range():
    """2. for文とrangeを使った繰り返し処理のデモ。"""
    print("=" * 60)
    print("[2] for + range : 複数サーバーのステータス確認ループ")
    print("=" * 60)

    # サーバー監視スクリプトでは「サーバーno.1〜no.5を順番にチェックする」
    # といった処理がよくある。range()を使うと簡潔に書ける。
    server_count = 5
    # 疑似的なチェック結果(本来はここでrequestsなどを使って通信するが、
    # このサンプルでは外部通信を行わないよう、あらかじめ結果を用意しておく)
    dummy_check_results = [True, True, False, True, False]

    ok_count = 0
    ng_count = 0

    for i in range(server_count):
        server_name = f"server-{i + 1:02d}"
        is_ok = dummy_check_results[i]

        if is_ok:
            print(f"  {server_name}: OK  (正常に応答しました)")
            ok_count += 1
        else:
            print(f"  {server_name}: NG  (応答がありませんでした)")
            ng_count += 1

    print(f"  -> 正常: {ok_count}台 / 異常: {ng_count}台")
    print()


def section3_while_break_continue():
    """3. while文とbreak/continueを使ったリトライ処理のデモ。"""
    print("=" * 60)
    print("[3] while + break/continue : 接続リトライのシミュレーション")
    print("=" * 60)

    # 1回目・2回目は失敗し、3回目で成功するケースをシミュレーションする
    is_success_sequence = [False, False, True]
    max_retries = 5

    attempt = 0
    while attempt < max_retries:
        # continueの例: 「0回目(=1回目の試行前)」のような無効な状態が
        # あった場合にスキップする、という状況を再現するダミー処理。
        # (このサンプルでは常にFalseなのでcontinueは実行されないが、
        #  continueの書き方を示すために残している)
        if attempt < 0:
            attempt += 1
            continue

        if attempt >= len(is_success_sequence):
            print("  試行データが尽きたため、リトライを終了します。")
            break

        print(f"  接続試行 {attempt + 1}回目...", end=" ")

        if is_success_sequence[attempt]:
            print("成功!")
            # breakの例: 成功したのでこれ以上リトライする必要がない
            break
        else:
            print("失敗。少し待って再試行します。")

        attempt += 1
    else:
        # while-elseは「breakされずにループが正常終了した場合」に実行される
        print("  max_retries回試しましたが、すべて失敗しました。")

    print()


def section4_aggregation():
    """4. リストに対するfor文での集計処理(稼働率の計算)のデモ。"""
    print("=" * 60)
    print("[4] for文での集計 : サーバー稼働率(アップタイム率)の計算")
    print("=" * 60)

    # 直近10回分のヘルスチェック結果(True=成功, False=失敗)
    check_results = [True, True, True, True, False, True, True, True, False, True]

    success_count = 0
    for result in check_results:
        if result:
            success_count += 1

    total = len(check_results)
    if total == 0:
        uptime_rate = 0.0
    else:
        uptime_rate = round(success_count / total * 100, 2)

    print(f"  チェック回数: {total}回")
    print(f"  成功回数    : {success_count}回")
    print(f"  稼働率      : {uptime_rate}%")
    print()


def main():
    """サンプルコード全体のエントリーポイント。"""
    section1_if_elif_else()
    section2_for_and_range()
    section3_while_break_continue()
    section4_aggregation()
    print("サンプルコードの実行が完了しました。演習にもぜひ挑戦してみてください!")


if __name__ == "__main__":
    main()

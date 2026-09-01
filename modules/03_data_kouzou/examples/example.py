"""
第3章: データ構造(list, dict, tuple, set, 内包表記, sorted) サンプルコード
==========================================================================

このファイルは、サーバー運用でよく使う「複数のデータをまとめて扱う方法」
(list, dict, tuple, set)と、それらを効率よく操作するための書き方
(リスト内包表記、in演算子、sorted()のkey引数、スライス)を
実際に動かしながら確認するためのサンプルです。

実行方法:
    cd /home/user/python
    python3 modules/03_data_kouzou/examples/example.py

外部ネットワークへのアクセスは一切行いません。すべてこのファイルの中だけで
完結するダミーデータ(疑似的なデータ)を使ってシミュレーションします。
"""


def section1_list_and_comprehension():
    """1. リスト(list)とリスト内包表記のデモ。"""
    print("=" * 60)
    print("[1] list とリスト内包表記 : 稼働中のサーバーを抜き出す")
    print("=" * 60)

    # サーバー監視でよくある「複数サーバーの状態」を表すリスト
    servers = [
        {"name": "web01", "status": "active"},
        {"name": "web02", "status": "stopped"},
        {"name": "db01", "status": "active"},
        {"name": "cache01", "status": "maintenance"},
    ]

    # for文で書くと、こうなる(演習1ではこれと同じことを内包表記で書く)
    active_names_for_loop = []
    for server in servers:
        if server["status"] == "active":
            active_names_for_loop.append(server["name"])

    # リスト内包表記を使うと、上のfor文を1行で書ける
    # 書式: [式 for 要素 in リスト if 条件]
    active_names = [s["name"] for s in servers if s["status"] == "active"]

    print(f"  for文で集めた結果      : {active_names_for_loop}")
    print(f"  内包表記で集めた結果   : {active_names}")
    print(f"  -> 稼働中のサーバー数: {len(active_names)}台")
    print()


def section2_dict_and_in():
    """2. 辞書(dict)とin演算子のデモ。"""
    print("=" * 60)
    print("[2] dict と in演算子 : サービス名とポート番号の対応表")
    print("=" * 60)

    # {サービス名: ポート番号} という対応表(マップ)は実務でも頻出のデータ形式
    service_ports = {
        "ssh": 22,
        "http": 80,
        "https": 443,
        "mysql": 3306,
    }

    # 辞書から値を取り出す(キーが存在しない場合にエラーを避けるため .get() を使う)
    print(f"  http のポート番号   : {service_ports.get('http')}")
    print(f"  ftp のポート番号    : {service_ports.get('ftp')}")  # 未登録なので None

    # in演算子でキーの存在チェックができる
    check_targets = ["ssh", "ftp", "https"]
    for name in check_targets:
        if name in service_ports:
            print(f"  '{name}' は登録済みのサービスです(ポート: {service_ports[name]})")
        else:
            print(f"  '{name}' は登録されていないサービスです")

    print()


def section3_tuple_and_set():
    """3. タプル(tuple)と集合(set)のデモ。"""
    print("=" * 60)
    print("[3] tuple と set : IPアドレスの重複除去とタプルの活用")
    print("=" * 60)

    # タプルは「変更しない値の組」を表すのによく使われる(例: 座標、名前とポートの組など)
    # ここでは (サービス名, ポート番号) というタプルのリストを辞書に変換する例を示す
    service_pairs = [("ssh", 22), ("http", 80), ("https", 443)]
    port_map = {}
    for name, port in service_pairs:  # タプルの中身を name, port にアンパック(分解)している
        port_map[name] = port
    print(f"  タプルのリストから作った辞書: {port_map}")

    # setは「重複しない値の集まり」。アクセスログのIPアドレスから
    # ユニーク(重複のない)IPアドレスの一覧を作りたいときによく使う
    access_log_ips = [
        "192.168.1.10",
        "10.0.0.5",
        "192.168.1.10",
        "10.0.0.5",
        "10.0.0.6",
    ]
    unique_ips = sorted(set(access_log_ips))
    print(f"  アクセスログ(重複あり) : {access_log_ips}")
    print(f"  重複除去 + 昇順ソート後  : {unique_ips}")
    print(f"  -> ユニークなアクセス元IP数: {len(unique_ips)}件")
    print()


def section4_sorted_and_slice():
    """4. sorted()のkey引数とスライスのデモ。"""
    print("=" * 60)
    print("[4] sorted() の key引数 とスライス : 負荷順ソート")
    print("=" * 60)

    # 各サーバーのCPU負荷(%)を表すデータ
    servers = [
        {"name": "web01", "cpu_load": 45.0},
        {"name": "web02", "cpu_load": 92.5},
        {"name": "db01", "cpu_load": 60.0},
        {"name": "cache01", "cpu_load": 15.5},
        {"name": "batch01", "cpu_load": 78.0},
    ]

    # sorted()のkey引数に「並べ替えの基準にしたい値」を返す関数(ここではlambda式)を渡す
    # reverse=True で降順(大きい順)にソートする
    sorted_by_load = sorted(servers, key=lambda s: s["cpu_load"], reverse=True)

    print("  CPU負荷が高い順にすべて表示:")
    for server in sorted_by_load:
        print(f"    {server['name']:<10} 負荷: {server['cpu_load']:>5.1f}%")

    # スライス([開始:終了])で「上位N件」だけを取り出す
    top3 = sorted_by_load[:3]
    print(f"\n  -> 上位3台(要対応の可能性が高いサーバー): "
          f"{[s['name'] for s in top3]}")
    print()


def main():
    """サンプルコード全体のエントリーポイント。"""
    section1_list_and_comprehension()
    section2_dict_and_in()
    section3_tuple_and_set()
    section4_sorted_and_slice()
    print("サンプルコードの実行が完了しました。演習にもぜひ挑戦してみてください!")


if __name__ == "__main__":
    main()

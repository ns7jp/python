"""
第5章: ファイル操作とOS操作(open, with文, pathlib.Path) サンプルコード
==========================================================================

このファイルは、サーバー運用の定番作業である「ログファイルの読み書き」と
「ディレクトリ内のファイルを調べる」処理を、実際に動かしながら確認するための
サンプルです。

実行方法:
    cd /home/user/python
    python3 modules/05_file_os_sousa/examples/example.py

外部ネットワークへのアクセスは一切行いません。すべて tempfile モジュールで
作成する一時ディレクトリの中だけでファイルの作成・読み書きを行い、
プログラムの終了時に自動的に片付けられるので、リポジトリの中には
何も残りません。安心して何度でも実行してみてください。
"""

import os
import tempfile
from datetime import datetime
from pathlib import Path


def section1_open_and_with(work_dir):
    """1. open()とwith文、書き込みモード(w, a)、読み込みモード(r)のデモ。"""
    print("=" * 60)
    print("[1] open() と with文 : ファイルの書き込みモードと読み込みモード")
    print("=" * 60)

    log_path = os.path.join(work_dir, "with_demo.log")

    # "w"モード(write): ファイルを新規作成、またはすでにある場合は中身を
    # まるごと上書きして空にする。設定ファイルを新しく作り直すときなどに使う。
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("1行目: サーバーを起動しました\n")
        f.write("2行目: 設定ファイルを読み込みました\n")
    print("  'w'モードで書き込み -> ファイルが新規作成され、2行が書き込まれた")

    # "a"モード(append): ファイルの末尾に追記する。すでにある内容は消えない。
    # ログファイルへの書き込みでは、こちらを使うのが定番。
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("3行目: リクエストを受け付けました\n")
    print("  'a'モードで追記      -> 既存の内容はそのままに、3行目が追加された")

    # "r"モード(read): 読み込み専用で開く。with文を使うと、処理が終わった
    # ときやエラーが起きたときも、自動的にファイルが閉じられるので安全。
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()  # 1行ずつ、改行付きの文字列としてリストで取得
    print(f"  'r'モードで読み込み  -> {len(lines)}行を読み込んだ:")
    for line in lines:
        print(f"    {line.rstrip()}")  # rstrip()で末尾の改行を除いて表示

    print(
        "\n  ポイント: with文を使わずに open()/close() を手動で呼び出すと、"
        "\n  途中でエラーが起きた場合に close() が呼ばれずファイルが"
        "\n  開きっぱなしになる危険がある。with文なら自動的に閉じてくれるので安全。"
    )
    print()


def section2_pathlib_basics(work_dir):
    """2. pathlib.Path の基本操作のデモ。"""
    print("=" * 60)
    print("[2] pathlib.Path : パスをオブジェクトとして扱う")
    print("=" * 60)

    # 文字列でパスを組み立てる代わりに、Pathオブジェクトを使うと
    # OSの違い(区切り文字が / か \ か)を気にせずパス操作ができる
    base_dir = Path(work_dir)
    log_path = base_dir / "logs" / "app.log"  # "/" 演算子でパスを連結できる

    print(f"  組み立てたパス       : {log_path}")
    print(f"  ファイル名(.name)   : {log_path.name}")
    print(f"  拡張子(.suffix)     : {log_path.suffix}")
    print(f"  親ディレクトリ(.parent): {log_path.parent}")
    print(f"  存在するか(.exists()): {log_path.exists()}  (まだ作っていないので False)")

    # ディレクトリを作成してからファイルを書き込んでみる
    log_path.parent.mkdir(parents=True, exist_ok=True)  # 途中のディレクトリもまとめて作成
    log_path.write_text("[INFO] pathlibで作成したログ\n", encoding="utf-8")
    print(f"  ディレクトリ作成 & 書き込み後の存在確認: {log_path.exists()}")

    # Pathオブジェクトは read_text() / write_text() で、
    # open()を使わずに手軽にファイルの読み書きができる
    content = log_path.read_text(encoding="utf-8")
    print(f"  read_text()での読み込み結果: {content.strip()!r}")
    print()


def section3_list_dir_and_stat(work_dir):
    """3. ディレクトリ内のファイル一覧、サイズ・更新日時の取得のデモ。"""
    print("=" * 60)
    print("[3] ディレクトリの一覧取得 と ファイルサイズ・更新日時")
    print("=" * 60)

    log_dir = Path(work_dir) / "server_logs"
    log_dir.mkdir(exist_ok=True)

    # サーバー運用でよくある「複数のログファイルが並んでいる」状態を再現する
    (log_dir / "access.log").write_text("access " * 20, encoding="utf-8")
    (log_dir / "error.log").write_text("error " * 80, encoding="utf-8")
    (log_dir / "debug.log").write_text("debug", encoding="utf-8")
    (log_dir / "readme.txt").write_text("これはログではないメモ", encoding="utf-8")

    # iterdir() で、ディレクトリ直下のファイル・サブディレクトリを一覧できる
    print("  ディレクトリ内のすべてのエントリ:")
    for entry in sorted(log_dir.iterdir()):
        kind = "ディレクトリ" if entry.is_dir() else "ファイル"
        print(f"    {entry.name:<15} ({kind})")

    # glob("*.log") を使うと、パターンに合うファイルだけを直接取り出せる
    print("\n  .log ファイルだけを抽出し、サイズと更新日時を表示:")
    log_files = list(log_dir.glob("*.log"))
    for entry in log_files:
        st = entry.stat()  # ファイルの情報(サイズ・更新日時など)をまとめて取得
        size = st.st_size  # バイト単位のファイルサイズ
        # st_mtime はエポック秒(1970年からの経過秒数)なので、
        # datetime.fromtimestamp() で人間が読める日時に変換する
        mtime = datetime.fromtimestamp(st.st_mtime)
        print(
            f"    {entry.name:<12} サイズ: {size:>6}バイト  "
            f"更新日時: {mtime.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    print()


def section4_log_cleanup_simulation(work_dir):
    """4. 古いログの整理(削除候補の一覧化)のシミュレーション。"""
    print("=" * 60)
    print("[4] 古いログ整理のシミュレーション : 削除候補を一覧するだけの安全な設計")
    print("=" * 60)

    cleanup_dir = Path(work_dir) / "rotate_logs"
    cleanup_dir.mkdir(exist_ok=True)

    # 更新日時が異なる5つのログファイルを用意する
    # (os.utime() で更新日時をわざと調整し、日々のログ生成を再現する)
    base_time = datetime.now().timestamp()
    file_specs = [
        ("app_2026-08-28.log", base_time - 4 * 86400),  # 4日前
        ("app_2026-08-29.log", base_time - 3 * 86400),  # 3日前
        ("app_2026-08-30.log", base_time - 2 * 86400),  # 2日前
        ("app_2026-08-31.log", base_time - 1 * 86400),  # 1日前
        ("app_2026-09-01.log", base_time),               # 今日(最新)
    ]
    for name, mtime in file_specs:
        file_path = cleanup_dir / name
        file_path.write_text(f"{name} の内容\n", encoding="utf-8")
        os.utime(file_path, (mtime, mtime))  # 更新日時を明示的に設定

    # 更新日時が新しい順に並べ替える
    log_files = list(cleanup_dir.glob("*.log"))
    log_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    max_files_to_keep = 3
    keep_files = log_files[:max_files_to_keep]
    delete_candidates = log_files[max_files_to_keep:]

    print(f"  ログファイル総数: {len(log_files)}件 / 残す件数: {max_files_to_keep}件")
    print("\n  残すファイル(新しい順):")
    for entry in keep_files:
        print(f"    KEEP     {entry.name}")

    print("\n  削除候補(古い順に残りすべて):")
    for entry in delete_candidates:
        print(f"    CANDIDATE {entry.name}")

    print(
        "\n  重要: このサンプルでは削除候補を『表示するだけ』で、"
        "\n  os.remove() などによる実際の削除は一切行っていません。"
        "\n  演習4の find_old_log_candidates() も同じ考え方で、"
        "\n  安全のため削除候補を返すだけの設計になっています。"
        "\n  実際に削除するかどうかは、一覧を人の目で確認したうえで"
        "\n  別の処理として判断するのが、運用の現場での基本的な流れです。"
    )
    print()


def main():
    """サンプルコード全体のエントリーポイント。"""
    # tempfile.TemporaryDirectory() は、withブロックを抜けるときに
    # 中身ごとディレクトリを自動的に削除してくれる。実験や検証のための
    # 一時的な作業ディレクトリを作るのに便利。
    with tempfile.TemporaryDirectory(prefix="ch05_example_") as work_dir:
        print(f"一時作業ディレクトリを作成しました: {work_dir}\n")

        section1_open_and_with(work_dir)
        section2_pathlib_basics(work_dir)
        section3_list_dir_and_stat(work_dir)
        section4_log_cleanup_simulation(work_dir)

    # withブロックを抜けた時点で、work_dir とその中身はすべて削除されている
    print("一時作業ディレクトリはプログラム終了時に自動的に削除されました。")
    print("サンプルコードの実行が完了しました。演習にもぜひ挑戦してみてください!")


if __name__ == "__main__":
    main()
